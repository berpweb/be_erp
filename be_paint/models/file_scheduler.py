import os
import base64
from datetime import datetime

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

from odoo import fields, models, api


class FileScheduler(models.Model):
    _name = "file.scheduler"

    @api.model
    def _check_location(self, path):
        return os.path.exists(path)

    @api.model
    def prepare_file_list(self, from_path):
        if self._check_location(from_path):
            file_list = [os.path.join(from_path, f) for f in os.listdir(from_path)]
            return file_list

    @api.model
    def process_paint_records(self, file_list):
        PaintProduct = self.env['paint.product']
        for f in file_list:
            with open(f, 'rb') as fp:
                data = base64.encodestring(fp.read())
                PaintProduct.create({
                    'name': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'data_file': data,
                    'filename': os.path.basename(fp.name)
                })
            os.remove(f)

    @api.model
    def process_paint_files(self):
        paint_file_location = self.env['ir.config_parameter'].get_param('be_paint.paint_file_location')
        if paint_file_location:
            file_list = self.prepare_file_list(paint_file_location)
            if file_list:
                self.process_paint_records(file_list)
        return True
