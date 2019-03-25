from django.db import models
from datetime import datetime

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email_id = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=13)
    
    class Meta:
        db_table = 'pos_users'
    
    def get_dict(self):
        return {
            'name': self.name,
            'email_id': self.email_id,
            'phone_number': 123
        }

class Item(models.Model):
    name = models.CharField(max_length=200, blank=False)
    brand = models.CharField(max_length=200, blank=False)
    category = models.CharField(max_length=200, blank=False)
    product_code = models.IntegerField(primary_key=True)
    created_by = models.ForeignKey('Users', on_delete='CASCADE', related_name='created_by')
    modified_by = models.ForeignKey('Users', on_delete='CASCADE', related_name='modified_by')

    class Meta:
        db_table = 'pos_invetory'

    def save(self, *args, **kwargs):
        fields_to_audit = [
            'name', 'brand', 'category', 'modified_by_id'
        ]
        try:
            existing_item = Item.objects.get(product_code=self.product_code)
            for field in fields_to_audit:
                if existing_item.__dict__[field] != self.__dict__[field]:
                    item_audit = {
                        'table_name': 'pos_invetory',
                        'changed_column': field,
                        'new_value': self.__dict__[field],
                        'old_value': existing_item.__dict__[field],
                        'change_type': 'Modified',
                        'modified_by_id': self.modified_by_id
                    }
                    audit  = Audit(**item_audit)
                    audit.save()
            item = super(Item, self).save(*args, **kwargs)
            return item
        except Item.DoesNotExist:
            item = super(Item, self).save(*args, **kwargs)
            for field in fields_to_audit:
                item_audit = {
                    'table_name': 'pos_invetory',
                    'changed_column': field,
                    'new_value': self.__dict__[field],
                    'old_value': self.__dict__[field],
                    'change_type': 'Created',
                    'modified_by_id': self.modified_by_id
                }
                audit  = Audit(**item_audit)
                audit.save()
            return item
        except Exception as e:
            raise e



class Variant(models.Model):
    SIZE_CHOISES = (
        ('L', 'Large'),
        ('M', 'Medium'),
        ('S', 'Small'),
        ('XL', 'Extra Large'),
    )
    name = models.CharField(max_length=200, blank=False)
    selling_price = models.FloatField()
    cost_price = models.FloatField()
    item = models.ForeignKey('Item', on_delete='CASCADE')
    size = models.CharField(max_length=25, choices=SIZE_CHOISES)
    options = models.CharField(max_length=25)
    quantity = models.IntegerField(default=0)
    created_by = models.ForeignKey('Users', on_delete='CASCADE', related_name='variant_created_by')
    modified_by = models.ForeignKey('Users', on_delete='CASCADE', related_name='variant_modified_by')

    class Meta:
        db_table = 'pos_variant'

    def save(self, *args, **kwargs):
        fields_to_audit = [
            'name', 'selling_price', 'cost_price', 'item_id', 'size', 'options', 'modified_by'
        ]

        try:
            if self.id is not None:
                existing_variant = Variant.objects.get(pk=self.id)
                for field in fields_to_audit:
                    if existing_variant.__dict__[field] != self.__dict__[field]:
                        item_audit = {
                            'table_name': 'pos_variant',
                            'changed_column': field,
                            'new_value': self.__dict__[field],
                            'old_value': existing_variant.__dict__[field],
                            'change_type': 'Modified',
                            'modified_by_id': self.modified_by_id
                        }
                        audit  = Audit(**item_audit)
                        audit.save()
                variant = super(Variant, self).save(*args, **kwargs)
                return variant
        except Variant.DoesNotExist:
            variant = super(Variant, self).save(*args, **kwargs)
            for field in fields_to_audit:
                item_audit = {
                    'table_name': 'pos_invpos_variantetory',
                    'changed_column': field,
                    'new_value': self.__dict__[field],
                    'old_value': self.__dict__[field],
                    'change_type': 'Created',
                    'modified_by_id': self.modified_by_id
                }
                audit  = Audit(**item_audit)
                audit.save()
            return variant
        except Exception as e:
            raise e

class Audit(models.Model):
    CHANGE_TYPES = (
        ('Create', 'Created'),
        ('Modified', 'Modified')
    )
    table_name = models.CharField(max_length=40, blank=False)
    changed_column = models.CharField(max_length=200, blank=False)
    new_value = models.CharField(max_length=200, blank=False)
    old_value = models.CharField(max_length=200, blank=True)
    modified_by = models.ForeignKey('Users', on_delete='CASCADE')
    modified_at = models.DateTimeField(default=datetime.now())
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPES)

    class Meta:
        db_table = 'pos_audit'
