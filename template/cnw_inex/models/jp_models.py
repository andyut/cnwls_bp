# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
from datetime import datetime
import pytz
from num2words import num2words
import pymssql
from odoo.exceptions import UserError
from odoo.modules import get_modules, get_module_path
import base64
from jinja2 import Environment, FileSystemLoader
import pdfkit
import os


class CNWJP(models.Model):
    _name           = "cnw.jp"
    _description    = "Jurnal Pemindahan"

    company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.user.company_id.id)    
    name            = fields.Char("Trans Number")
    refdate         = fields.Date("Doc Date",required=True,default=lambda s:fields.Date.today())
    remarks1         = fields.Text("Remarks1",required=True)  
    credittotal     = fields.Float("Credit",digit=(19,0),default=0,required=True)
    debettotal      = fields.Float("Debet",digit=(19,0),default=0,required=True)

    itype           = fields.Selection(string="Type",selection=[("BANK","Bank"),("CASH","Cash"),("OTHERES","Others")] ,default="BANK") 

    partner         = fields.Char("Partner")

    creator         = fields.Many2one("res.users")
    approval        = fields.Many2one("res.users")

    status          =  fields.Selection(string="Status",selection=[("draft","Draft"),
                                                                        ("pending","Waiting Approval"),
                                                                        ("posted","Posted"),
                                                                        ("cancel","Canceled"),
                                                                        ("reqcancel","Request Cancel"),],
                                                                        default="draft")


    jpline_ids      = fields.One2many("cnw.jp.line","jp_id")


    filexls         = fields.Binary("File Output")    
    filenamexls     = fields.Char("File Name Output")
    
    @api.onchange("jpline_ids")
    def calculate_total(self):
        self.debettotal = 0
        self.credittotal = 0
        self.amount = 0

        for line in self.jpline_ids:

            self.debettotal += line.debit
            self.credittotal += line.credit 



    @api.model
    def create(self,vals):
        numbering  = self.env["cnw.numbering.wizard"].getnumbering('JPV',datetime.strptime(vals["refdate"],'%Y-%m-%d'))
        print(numbering)
        vals["name"] = numbering
        vals["status"] = "pending"
        vals["creator"] = self.env.user.id
        result = super(CNWJP,self).create(vals)
        return result

    def approve(self):
        self.status = "posted"
        self.approval = self.env.user.id
 

    def print_kasbon(self):
        mpath       = get_module_path('cnw_inex') 
        filenamepdf    = 'JPV_'+   self.name  + self.company_id.code_base + '.pdf' 
        filepath    = mpath + '/temp/'+ filenamepdf

#LOGO CSS AND TITLE
        logo        = mpath + '/template/logo'+ self.company_id.code_base + '.png' 
        #cssfile     = mpath + '/template/style.css'        
 
        options = { 
                    'page-size':'A4', 
                    'orientation': 'portrait',
                    }
        print_date = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d %H:%M:%S")
#2008202239

#MULTI COMPANY 
        

        env = Environment(loader=FileSystemLoader(mpath + '/template/'))
        
        template = env.get_template("jp.html")     

#collecting Data

        remarks1 = self.remarks1 if self.remarks1 else ""
        partner = self.partner if self.partner else ""

        
        detail=[]
        for jpline in self.jpline_ids:
            remarks = jpline.acctcode + ' - ' + jpline.remarks if jpline.remarks else jpline.account.name
            line =[]
            debit = jpline.debit 
            credit = jpline.credit 
            line.append(remarks)
            line.append(debit)
            line.append(credit)
            detail.append(line)
        
        print(detail)


        template_var    = { "company":self.company_id.name, 
                            "logo":logo,
                            "name":self.name,
                            "location":"Jakarta", 
                            "refdate" :self.refdate, 
                            "datetime" : datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d %H:%M:%S") , 
                            "partner" : partner,
                            "remarks1" :remarks1 ,  
                            "debettotal" :"{0:,.2f}".format(self.debettotal),  
                            "credittotal" :"{0:,.2f}".format(self.credittotal),  
                            "detail" : detail,
                            "approval":self.approval.name ,
                            "creator":self.creator.name ,}


        html_out = template.render(template_var)
        
        pdfkit.from_string(html_out,mpath + '/temp/'+ filenamepdf,options=options) 
        
       # SAVE TO MODEL.BINARY 
        file = open(mpath + '/temp/'+ filenamepdf , 'rb')
        out = file.read()
        file.close()
        self.filexls =base64.b64encode(out)
        self.filenamexls = filenamepdf
        os.remove(mpath + '/temp/'+ filenamepdf )
        return {
            'name': 'Report',
            'type': 'ir.actions.act_url',
            'url': "web/content/?model=" + self._name +"&id=" + str(
                self.id) + "&filename_field=filenamexls&field=filexls&download=true&filename=" + self.filenamexls,
            'target': 'new',
            }        



class CNWJPAccount(models.Model):
    _name  = "cnw.jp.account"
    _description = "JP Account"
    company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.user.company_id.id)    
    name            = fields.Char("Account")
    acctcode        = fields.Char("Account")


    
class CNWJPLine(models.Model):
    _name = "cnw.jp.line"
    _description = "Jurnal Pemindahan Line"
    company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.user.company_id.id)    

    account         = fields.Many2one("cnw.jp.account" ,required=True)
    acctcode        = fields.Char("Acct Code" ,related="account.acctcode",required=True)
    remarks         = fields.Char("Remarks")
    debit           = fields.Float("Debet",digit=(19,0),default=0,required=True)
    credit          = fields.Float("Credit",digit=(19,0),default=0,required=True)
    amount          = fields.Float("Amount",digit=(19,0),default=0,required=True)

    jp_id           = fields.Many2one("cnw.jp")


    @api.onchange("debit","credit")
    def calculate_amount(self):
        self.amount = self.debit - self.credit