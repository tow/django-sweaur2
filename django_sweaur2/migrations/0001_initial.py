# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RefreshToken'
        db.create_table('django_sweaur2_refreshtoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token_string', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('scope', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('django_sweaur2', ['RefreshToken'])

        # Adding model 'AccessToken'
        db.create_table('django_sweaur2_accesstoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token_string', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('scope', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('expires_in', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('old_refresh_token', self.gf('django.db.models.fields.related.OneToOneField')(related_name='new_access_token', unique=True, null=True, to=orm['django_sweaur2.RefreshToken'])),
            ('new_refresh_token', self.gf('django.db.models.fields.related.OneToOneField')(related_name='old_access_token', unique=True, null=True, to=orm['django_sweaur2.RefreshToken'])),
            ('token_type_id', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('extra_parameters', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('django_sweaur2', ['AccessToken'])


    def backwards(self, orm):
        
        # Deleting model 'RefreshToken'
        db.delete_table('django_sweaur2_refreshtoken')

        # Deleting model 'AccessToken'
        db.delete_table('django_sweaur2_accesstoken')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'django_sweaur2.accesstoken': {
            'Meta': {'object_name': 'AccessToken'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'expires_in': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'extra_parameters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_refresh_token': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'old_access_token'", 'unique': 'True', 'null': 'True', 'to': "orm['django_sweaur2.RefreshToken']"}),
            'old_refresh_token': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'new_access_token'", 'unique': 'True', 'null': 'True', 'to': "orm['django_sweaur2.RefreshToken']"}),
            'scope': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'token_string': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'token_type_id': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'django_sweaur2.refreshtoken': {
            'Meta': {'object_name': 'RefreshToken'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scope': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'token_string': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        }
    }

    complete_apps = ['django_sweaur2']
