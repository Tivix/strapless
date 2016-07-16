from __future__ import absolute_import
import random, string

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    __LOREM_IPSUM = """Auctor et. Adipiscing vut, sociis duis, quis tincidunt! Magna. Montes phasellus adipiscing platea elementum arcu in ut rhoncus, est lacus scelerisque auctor placerat magna! Amet turpis urna mattis! Nunc rhoncus! Massa non, sit aliquam massa. Sit enim in? Sed massa ac, lundium aenean dapibus, pellentesque ut odio nascetur? Auctor turpis. Magna? Etiam amet eros, elementum, parturient magna et ut? Ac vel tortor aenean. Ut ut velit scelerisque tortor nec a lundium. In sit odio, pellentesque tristique, nunc ultrices amet dolor aliquam integer mattis, tempor magna diam et sed in turpis rhoncus et? Nascetur elementum mauris vel rhoncus, aliquet a. Porttitor ridiculus ac penatibus pulvinar enim sociis? Aliquam duis sed augue augue dis nunc porttitor tortor turpis dapibus urna, et risus augue etiam non lundium! A, magnis tincidunt tincidunt. Elementum sit, pellentesque lectus elementum integer. Diam scelerisque magnis augue, cum? A scelerisque natoque purus amet amet in aliquam ac. Tincidunt natoque, rhoncus vel aliquet porttitor dolor etiam augue? Habitasse pulvinar, a, montes lorem, elementum! Mattis placerat, in et amet magnis, eros porta? Ultrices? Hac auctor mid? Risus hac ut, placerat porta? Dignissim lorem in ac odio? Egestas nunc amet dictumst. Sagittis magnis cras et! Tincidunt est. Mattis mattis. Tristique, non ac, ac a turpis ultrices integer eu aliquam tempor vut! Cursus platea lacus amet! Dolor mattis enim est ut ac adipiscing sed, penatibus montes quis turpis, sit odio proin ac tincidunt placerat habitasse dolor, ridiculus aenean scelerisque odio? Egestas lacus integer, lundium, tempor! Ridiculus turpis parturient lacus eu."""

    __NUM_USERS = 300
    def handle(self, *args, **options):
        #clean up old stuff
        get_user_model().objects.filter(is_superuser=False).delete()
        #then Create fakedata
        pass

    def __random_spaced_string(self, max_length):
        return ' '.join(random.sample(self.__LOREM_IPSUM.split(' '), max_length/5))[:max_length]

    def __random_string(self, max_length):
        return ''.join([random.choice(string.letters) for x in range(0, max_length)])

    def __random_digit_string(self, max_length):
        return ''.join([str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) for x in range(0, max_length)])
