import copy
import datetime
import pytz

import parsekit


class AddTimestamp(parsekit.Step):

    def configure(self, options):
        self.tz = pytz.timezone('UTC')

    def run(self, record, metadata):
        schema = copy.deepcopy(metadata.get_closest('schema'))
        ts = self.tz.localize(datetime.datetime.now())
        record.append(ts)
        schema.append_field(parsekit.schema.DateTimeField('last_updated'))
        metadata['schema'] = schema
        return record, metadata
