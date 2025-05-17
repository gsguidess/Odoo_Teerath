from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TodoTag(models.Model):
    _name = 'todo.tag'
    _description = 'Todo Tag'

    name = fields.Char(required=True, unique=True)

class TodoList(models.Model):
    _name = 'todo.list'
    _description = 'Todo List'
    _order = 'start_date'

    name = fields.Char(string='Title', required=True)
    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)

    status = fields.Selection([('draft', 'Draft'), ('in_progress', 'In Progress'), ('complete', 'Complete')], default='draft')
    
    #TodoTag
    tag_ids = fields.Many2many('todo.tag', string='Tags')
    tag_names = fields.Char(string='Tags', compute='_compute_tag_names', store=True)

    #TodoProgress
    progress_ids = fields.One2many('todo.progress', 'todo_id', string="Progress")
    
    #TodoLine
    line_ids = fields.One2many('todo.line', 'todo_id', string='Tasks')
    description = fields.Text(string="Description")

    #TodoAttendee
    attendee_ids = fields.One2many('todo.attendee', 'todo_id', string='Attendees')

    #done
    all_done = fields.Boolean(compute='_compute_all_done', store=True)

            
    @api.depends('line_ids.done')
    def _compute_all_done(self):
        for record in self:
            record.all_done = all(line.done for line in record.line_ids)
    
    def action_button_done(self):
        for rec in self:
            if rec.all_done:
                rec.status = 'complete'
                
    @api.depends('tag_ids')
    def _compute_tag_names(self):
        for record in self:
            record.tag_names = ', '.join(record.tag_ids.mapped('name'))

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date <= rec.start_date:
                raise ValidationError('End date must be after start date.')


    def action_button_draft(self):
        self.write({'status': 'draft'})

    def action_button_inprogress(self):
        self.write({'status': 'in_progress'})

    def action_button_complete(self):
        self.write({'status': 'complete'})

class TodoProgress(models.Model):
    _name = 'todo.progress'
    _description = 'Todo Progress'

    name = fields.Char("Detail")
    todo_id = fields.Many2one('todo.list', string="Todo List", ondelete='cascade')

class TodoLine(models.Model):
    _name = 'todo.line'
    _description = 'To-Do Line'

    todo_id = fields.Many2one('todo.list', string='To-Do List', ondelete='cascade')
    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    done = fields.Boolean(string='Is complete')
    
class TodoAttendee(models.Model):
    _name = 'todo.attendee'
    _description = 'Todo Attendee'

    todo_id = fields.Many2one('todo.list', string='Todo List')
    user_id = fields.Many2one('res.users', string='Attendee', required=True)