# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

# We monkey patch pre 0.8 south to avoid a problem with this migration failing
# See issue #48
from south import __version__
if not __version__.startswith('0.8'):
    from south.db import mysql
    def _lookup_constraint_references(self, table_name, cname):
        """
        Provided an existing table and constraint, returns tuple of (foreign
        table, column)
        """
        db_name = self._get_setting('NAME')
        try:
            return self._constraint_references[db_name][(table_name, cname)]
        except KeyError:
            raise IndexError  # would normally return None, see upstream #1186
    mysql.DatabaseOperations._lookup_constraint_references = _lookup_constraint_references

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('hwdoc_equipment', 'temp_id', 'state_id')

    def backwards(self, orm):
        db.rename_column('hwdoc_equipment', 'state_id', 'temp_id')

    models = {
        'hwdoc.email': {
            'Meta': {'object_name': 'Email'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'hwdoc.equipment': {
            'Meta': {'object_name': 'Equipment'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'allocation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hwdoc.Project']", 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hwdoc.Model']"}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'rack': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'default': '5', 'to': "orm['hwdoc.State']"}),
            'unit': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'hwdoc.model': {
            'Meta': {'object_name': 'Model'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'u': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hwdoc.Vendor']"})
        },
        'hwdoc.person': {
            'Meta': {'object_name': 'Person'},
            'emails': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['hwdoc.Email']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'phones': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['hwdoc.Phone']", 'symmetrical': 'False'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'hwdoc.phone': {
            'Meta': {'object_name': 'Phone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'hwdoc.project': {
            'Meta': {'object_name': 'Project'},
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['hwdoc.Person']", 'through': "orm['hwdoc.Role']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'hwdoc.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hwdoc.Person']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hwdoc.Project']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'hwdoc.servermanagement': {
            'Meta': {'object_name': 'ServerManagement'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'equipment': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['hwdoc.Equipment']", 'unique': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'mac': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'raid_license': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'})
        },
        'hwdoc.state': {
            'Meta': {'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'hwdoc.vendor': {
            'Meta': {'object_name': 'Vendor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['hwdoc']
