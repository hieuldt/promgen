# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 03:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import json


def convert_to_list(apps, schema_editor):
    Rule = apps.get_model('promgen', 'Rule')
    Label = apps.get_model('promgen', 'RuleLabel')
    Annotation = apps.get_model('promgen', 'RuleAnnotation')

    for rule in Rule.objects.all():
        for k, v in json.loads(rule.labels).items():
            Label.objects.create(name=k, value=v, rule=rule)
        for k, v in json.loads(rule.annotations).items():
            Annotation.objects.create(name=k, value=v, rule=rule)


def convert_to_json(apps, schema_editor):
    Rule = apps.get_model('promgen', 'Rule')
    Label = apps.get_model('promgen', 'RuleLabel')
    Annotation = apps.get_model('promgen', 'RuleAnnotation')

    for rule in Rule.objects.all():
        rule.labels = json.dumps({
            obj.name: obj.value for obj in Label.objects.filter(rule=rule)
        })
        rule.annotations = json.dumps({
            obj.name: obj.value for obj in Annotation.objects.filter(rule=rule)
        })
        rule.save()


class Migration(migrations.Migration):

    dependencies = [
        ('promgen', '0023_shard'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuleAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RuleLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('value', models.CharField(max_length=128)),
            ],
        ),

        migrations.AddField(
            model_name='rulelabel',
            name='rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promgen.Rule'),
        ),
        migrations.AddField(
            model_name='ruleannotation',
            name='rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='promgen.Rule'),
        ),

        migrations.RunPython(convert_to_list, convert_to_json, elidable=True),

        migrations.RemoveField(
            model_name='rule',
            name='annotations',
        ),
        migrations.RemoveField(
            model_name='rule',
            name='labels',
        ),

    ]
