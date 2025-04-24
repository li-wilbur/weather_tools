class SimpleView:
    def __init__(self, view_type='shell'):
        self.view_type = view_type


    def view(self,data):
        view_type = self.view_type
        print(view_type)
        #print(data)
        for d in data:
            for d1 in d.values():
                try:
                    for k,v in d1['now'].items():
                        print(k,v)
                except KeyError as e:
                    print('Missing key:',e)
                    for k,v in d1.items():
                        print(k,v)