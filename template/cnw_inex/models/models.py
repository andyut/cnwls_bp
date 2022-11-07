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

class CNWInex(models.Model):
    _name           = "cnw.inex"
    _description    = "Income Expense Payment"

    company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.user.company_id.id)    
    name            = fields.Char("Trans Number")
    refdate         = fields.Date("Doc Date",required=True,default=lambda s:fields.Date.today())
    remarks1         = fields.Char("Remarks1",required=True)
    remarks2         = fields.Char("Remarks2")
    remarks3         = fields.Char("Remarks3")
    remarks4         = fields.Char("Remarks4")
    terbilang       = fields.Char("Terbilang",required=True)
    jenis           =  fields.Selection(string="Jenis",selection=[("PENGELUARAN","Pengeluaran"),
                                                                        ("PENERIMAAN","Penerimaan"),],
                                                                        default="PENGELUARAN")    
    amount          = fields.Float("Amount",digit=(19,0),default=0,required=True)
    itype           = fields.Selection(string="Type",selection=[("BANK","Bank"),("CASH","Cash"),("OTHERES","Others")] ,default="BANK")
    ref             = fields.Char("Ref",required=True,help="Bank Number / payment ref Number")
    partner         = fields.Char("Partner")

    creator         = fields.Many2one("res.users")
    approval        = fields.Many2one("res.users")

    status          =  fields.Selection(string="Status",selection=[("draft","Draft"),
                                                                        ("pending","Waiting Approval"),
                                                                        ("posted","Posted"),
                                                                        ("cancel","Canceled"),
                                                                        ("reqcancel","Request Cancel"),],
                                                                        default="draft")



    filexls         = fields.Binary("File Output")    
    filenamexls     = fields.Char("File Name Output")
    

    @api.model
    def create(self,vals):
        numbering  = self.env["cnw.numbering.wizard"].getnumbering('PYT',datetime.strptime(vals["refdate"],'%Y-%m-%d'))
        print(numbering)
        vals["name"] = numbering
        vals["status"] = "pending"
        vals["creator"] = self.env.user.id
        result = super(CNWInex,self).create(vals)
         
        return result

    def approve(self):
        self.status = "posted"
        self.approval = self.env.user.id

    @api.onchange("amount")
    def hitungTerbilang(self):
        if self.amount.is_integer():
            amount = int(self.amount)
        else:
            amount = self.amount
            
        self.terbilang = num2words(amount, lang="id")

        #self.terbilang = self._getterbilang()



    def print_kasbon(self):
        mpath       = get_module_path('cnw_inex') 
        filenamepdf    = 'kasbon_'+   self.name  + self.company_id.code_base + '.pdf' 
        filepath    = mpath + '/temp/'+ filenamepdf

#LOGO CSS AND TITLE
        logo        = mpath + '/template/logo'+ self.company_id.code_base + '.png' 
        #cssfile     = mpath + '/template/style.css'        
        options = { 
                    'page-size':'A5',
                    'orientation': 'landscape',
                    }
        options2 = { 
                    'page-size':'A4', 
                    'orientation': 'portrait',
                    }
        print_date = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d %H:%M:%S")
#2008202239

#MULTI COMPANY 
 

        env = Environment(loader=FileSystemLoader(mpath + '/template/'))
        
        template = env.get_template("kasbon.html")        
        remarks1 = self.remarks1 if self.remarks1 else ""
        remarks2 = self.remarks2 if self.remarks2 else ""
        remarks3 = self.remarks3 if self.remarks3 else ""

        template_var    = { "company":self.company_id.name, 
                            "logo":logo,
                            "name":self.name,
                            "location":"Jakarta", 
                            "refdate" :self.refdate,
                            "ref" :self.ref, 
                            "jenis":self.jenis,
                            "itype" : self.itype,  
                            "datetime" : datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d %H:%M:%S") , 
                            "remarks1" :remarks1 , 
                            "remarks2" :remarks2 , 
                            "remarks3" :remarks3 , 
                            "amount" :"{0:,.2f}".format(self.amount),  
                            "terbilang" :self.terbilang,
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