# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BearerRefreshToken'
        db.create_table('django_sweaur2_bearerrefreshtoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token_string', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('expires_in', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('django_sweaur2', ['BearerRefreshToken'])

        # Adding model 'BearerAccessToken'
        db.create_table('django_sweaur2_beareraccesstoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token_string', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('expires_in', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('old_refresh_token', self.gf('django.db.models.fields.related.OneToOneField')(related_name='new_access_token', unique=True, null=True, to=orm['django_sweaur2.BearerRefreshToken'])),
            ('new_refresh_token', self.gf('django.db.models.fields.related.OneToOneField')(related_name='old_access_token', unique=True, null=True, to=orm['django_sweaur2.BearerRefreshToken'])),
        ))
        db.send_create_signal('django_sweaur2', ['BearerAccessToken'])

        # Adding model 'MACRefreshToken'
        db.create_table('django_sweaur2_macrefreshtoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token_string', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('expires_in', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('django_sweaur2', ['MACRefreshToken'])

        # Adding model 'MACAccessToken'
        db.create_table('django_sweaur2_macaccesstoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token_string', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('expires_in', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('old_refresh_token', self.gf('django.db.models.fields.related.OneToOneField')(related_name='new_access_token', unique=True, null=True, to=orm['django_sweaur2.MACRefreshToken'])),
            ('new_refresh_token', self.gf('django.db.models.fields.related.OneToOneField')(related_name='old_access_token', unique=True, null=True, to=orm['django_sweaur2.MACRefreshToken'])),
            ('secret_token_string', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('algorithm', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('django_sweaur2', ['MACAccessToken'])


    def backwards(self, orm):
        
        # Deleting model 'BearerRefreshToken'
        db.delete_table('django_sweaur2_bearerrefreshtoken')

        # Deleting model 'BearerAccessToken'
        db.delete_table('django_sweaur2_beareraccesstoken')

        # Deleting model 'MACRefreshToken'
        db.delete_table('django_sweaur2_macrefreshtoken')

        # Deleting model 'MACAccessToken'
        db.delete_table('django_sweaur2_macaccesstoken')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'django_sweaur2.beareraccesstoken': {
            'Meta': {'object_name': 'BearerAccessToken'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'expires_in': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_refresh_token': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'old_access_token'", 'unique': 'True', 'null': 'True', 'to': "orm['django_sweaur2.BearerRefreshToken']"}),
            'old_refresh_token': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'new_access_token'", 'unique': 'True', 'null': 'True', 'to': "orm['django_sweaur2.BearerRefreshToken']"}),
            'token_string': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        },
        'django_sweaur2.bearerrefreshtoken': {
            'Meta': {'object_name': 'BearerRefreshToken'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'expires_in': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token_string': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        },
        'django_sweaur2.macaccesstoken': {
            'Meta': {'object_name': 'MACAccessToken'},
            'algorithm': ('django.db.models.fields.SmallIntegerField', [], {}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'expires_in': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_refresh_token': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'old_access_token'", 'unique': 'True', 'null': 'True', 'to': "orm['django_sweaur2.MACRefreshToken']"}),
            'old_refresh_token': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'new_access_token'", 'unique': 'True', 'null': 'True', 'to': "orm['django_sweaur2.MACRefreshToken']"}),
            'secret_token_string': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'token_string': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        },
        'django_sweaur2.macrefreshtoken': {
            'Meta': {'object_name': 'MACRefreshToken'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'expires_in': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token_string': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        }
    }

    complete_apps = ['django_sweaur2']
