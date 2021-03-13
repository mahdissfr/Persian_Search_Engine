import numpy as np


class ConstantVars():
    def __init__(self):
        self.punctuationMarks = ['.', '…', '،', ':', '؛', '\'', '@', '$', '/', ',', '(', ')', '[', ']', '`', '<', '>',
                          '?', '📌', '؟', '~', '&', '-', '_', ',', '،']

        self.stopWords = np.array(['و','در','به','از','که','این','را','با','برای','آن','تا','بر','هم','نیز','وی','اما','یا','باید',
        'هر','آنها','او','دیگر','پس','اگر','همه','یکی','چه','بی','همین','هایی','همچنین','روی','بیشتر','بسیار','چند','سوی','تنها',
        'برخی','بیش','چنین','طور','اینکه','بعد','ولی','حتی','کدام','سبب','عین','اغلب','دوباره','لذا','اینجا','هیچ','امر','زیرا',
        'درباره','بسیاری','چون','طی','حدود','همان','بدون','البته','دیگری','قابل','یعنی','کل','قبل','براساس','هنوز','کلی',
        'لازم','چرا','وقتی','کم','جای','اکنون','تحت','باعث','مدت','فقط','زیادی','آیا','عدم','نوع','بلکه','برابر','اخیر','مربوط',
        'زیر','شاید','خصوص','اثر','سایر','ضمن','مانند','ممکن','دارای','پی','مثل','کسی','آنچه','جمع','خیلی','علاوه','تاکنون',
        'مشخص','غیر','آخرین','شامل','تمامی','بهتر','کسانی','علیه','ناشی','حداقل','طبق','نوعی','چگونه','هنگام','فوق','روش'
        ,'همچنان','زیاد','سمت','کوچک','چیز','حالا','جایی','سپس','خودش','همواره','کمی','کاملا','نظیر',
                                  'ها','خویش','ترین','تر'])

    def punctuations(self):
        return self.punctuationMarks

    def StopWords(self):
        return self.stopWords
