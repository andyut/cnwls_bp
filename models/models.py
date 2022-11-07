# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
from datetime import datetime 
import pymssql
from odoo.exceptions import UserError
from odoo.modules import get_modules, get_module_path



class SAPPartnerTermPayment(models.Model):
    _name           = "cnwls.bp.termpayment"
    _description    = "CNWLS TERM PAYMENT"
    company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.user.company_id.id)
    name            = fields.Char("Term Of Payment")
    days            = fields.Integer("Days")
    sapid           = fields.Char("SAP ID")

class SAPPartnerGroup(models.Model):
    _name           = "cnwls.bp.groups"
    _description    = "CNWLS GROUP"
    company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.user.company_id.id)
    name            = fields.Char("Group Name")
    sapid           = fields.Char("SAP ID")

class SAPPartnerContact(models.Model):
    _name           = "cnwls.bp.contacts"
    _description    = "CNWLS BP Contact"
    company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.user.company_id.id)
    name            = fields.Char("Group Name")
    position        = fields.Char("Position")
    phone1          = fields.Char("Phone1")
    phone2          = fields.Char("Phone2")
    email           = fields.Char("Email ")
    nik             = fields.Char("NIK")
    address         = fields.Char("Address")
    sapid           = fields.Char("SAP ID")
    


class SAPPartnerOutlet(models.Model):
    _name           = "cnwls.bp.outlet"
    _description    = "CNWLS BP Outlet"
    company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.user.company_id.id)
    name            = fields.Char("Outlet Name")
    address         = fields.Char("Address")
    route           = fields.Char("Delivery Route")
    sapid           = fields.Char("SAP ID")

class SAPPartner(models.Model):
    _name           = "cnwls.bp"
    _description    = "SAP Business Partner"
    name            = fields.Char("Internal Code")
    company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.user.company_id.id)
    cardcode        = fields.Char("BP Code", default="BP Code")
    cardname        = fields.Char("BP Name" ,default="BP Name")
    cardfname       = fields.Char("BP Foreign Name",default="BP Foreign Name")
    partnerdesc     = fields.Char("Partner Long Desc",compute="_getdesc",store=True)
    groupname       = fields.Char("Group Name",default="Group Name")
    lictradnum      = fields.Char("Tax ID / NPWP")
    alamatnpwp      = fields.Char("Alamat NPWP", default="Alamat NPWP")
    ar_person       = fields.Char("AR Person", default="")
    salesperson     = fields.Char("Sales Person",default="Sales Person")
    salesgroup      = fields.Char("Sales Group",default="Sales Group")
    lock_limit      = fields.Char("Lock Limit in Month(s)")
    lock_bp         = fields.Char("Lock BP")
    paymentgroup    = fields.Char("Payment Group")
    creditline      = fields.Float("Credit Limit",digit=(19,6),default=0.0)
    balance         = fields.Float("Total Balance",digit=(19,6),default=0.0)
    b60             = fields.Float("Before 60 Days",digit=(19,6),default=0.0)
    a60             = fields.Float("After 60 Days",digit=(19,6),default=0.0)
    delivery        = fields.Float("Open Delivery",digit=(19,6),default=0.0)
    ordersbal       = fields.Float("Open Order",digit=(19,6),default=0.0)
    phone1          = fields.Char("Phone 1",default="")
    phone2          = fields.Char("Phone 2",default="")
    cellular        = fields.Char("Cellular",default="")    
    fax             = fields.Char("Fax",default="")
    e_mail          = fields.Char("E-Mail",default="")
    intrntsite      = fields.Char("Website",default="")
    notes           = fields.Char("Notes / Remarks",default="")
    cntctprsn       = fields.Char("Contact Person", default="")
    billaddress     = fields.Char("Billing Address",default="")
    address         = fields.Char("Address",default="")
    mailaddress     = fields.Char("Mail Address",default="") 
#follow up 
    laststatus      = fields.Char("Last Status")
    laststatus_date = fields.Datetime("Last Status Date")   
    followup_type   = fields.Selection(selection=[("mail","E-Mail"),("phone","Phone"),("whatsapp","Whatsapp"),("others","Other")],string="Type")
    followup_by     = fields.Selection(selection=[("ar","Follow Up By AR"),("sales","Follow Up By Sales"),("debt_collector","Follow Up By Debt Collector (Iwan)")],string="Follow Up By",default="ar")

    followup_ids    = fields.One2many("cnw.cflwup.followup","customer_id","Follow Up" )