from rest_framework import serializers,exceptions

from api.models import Books, Press


class PressModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=Press
        fields=('press_name','press_address')

class BookModelSerializer(serializers.ModelSerializer):
    press =PressModelSerializer()
    class Meta:
        model=Books
        # fields=('book_name','price','press_name','press_address','author_list')
        fields=('book_name','price','author_list','press')
        # depth=1




class BookDeModelSerializer(serializers.ModelSerializer):
    # press =PressModelSerializer()
    class Meta:
        model=Books
        # fields=('book_name','price','press_name','press_address','author_list')
        fields=('book_name','price','press','authors')
        # depth=1

        extra_kwargs = {
            'book_name': {
                'required': True,
                'min_length': 3,
                'error_messages': {
                    'required': '图书名必填',
                    'min_length': '书名太短'
                }
            },
            'press_name': {
                'write_only': True
            },
            'press_address': {
                'read_only': True
            }
        }

    def validate_book_name(self, value):
        if '1' in value:
            raise exceptions.ValidationError('图书名有误')
        return value

    def validate(self, attrs):
        price = attrs.get('price')
        if price > 100:
            raise exceptions.ValidationError('价格过高')
        return attrs