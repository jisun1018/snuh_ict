# 클래스 설계와 사용
# 코드 재사용성을 위함


##############
#User 클래스 생성
class User:
    def __init__(self, name, is_admin=False):
        self.name = name
        self.is_admin = is_admin


#User로부터 상속받는 3개의 클래스를 정의

class Admin(User):
    def __init__(self, name):
        super().__init__(name, is_admin=True)
        self.purchases = []

class Vendor(User):
    def __init__(self, name):
        super()._init__(name)
        self.products = [] 
    