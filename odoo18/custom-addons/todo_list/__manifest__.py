# -*- coding: utf-8 -*-
{
    'name': 'todo list',
    'version': '1.0',
    'summary': 'Organize your work with memos and to-do lists',
    'sequence': 10,
    'description': """
descriptiondescriptiondescriptiondescription
    """,
    'category': 'TodoList',
    'website': 'https://www.odoo.com',
    'author': 'Teerath Jantarux',
    'depends': [],
    'data': [
        "security/ir.model.access.csv",
        "data/todo_tags.xml",
        "views/todo_views.xml",
        "views/todo_menus.xml",
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'assets': {},
    'license': 'LGPL-3',
}
