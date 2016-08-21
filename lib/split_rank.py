import copy

import parsekit


class SplitRank(parsekit.Step):

    def run(self, record, metadata):
        schema = copy.deepcopy(metadata.get_closest('schema'))
        field_idx = schema.field_index('name')
        if record[field_idx]:
            parts = record[field_idx].split("|")
            record[field_idx] = parts[1]
            record.append(parts[0])
            schema.append_field(parsekit.schema.StringField('rank'))
            metadata['schema'] = schema
            return record, metadata
