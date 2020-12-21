'''
单例模式:
    单例模式是一个软件的设计模式，为了保证一个类，无论调用多少次产生的实例对象，
    都是指向同一个内存地址，仅仅只有一个实例(对象)!

    五种单例:
        - 模块
        - 装饰器
        - 元类
        - __new__
        - 类方法: classmethod
'''


class People:
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex


# 调用三次相同的类，传递相同的参数，产生不同的三个实例
p1 = People('tank', 17, 'male')
p2 = People('tank', 17, 'male')
p3 = People('tank', 17, 'male')
# print(p1 is p2 is p3)

# 打开同一个文件的时候，链接MySQL数据库
''' 伪代码
mysql_obj1 = MySQL(ip, port)
mysql_obj2 = MySQL(ip, port)
mysql_obj3 = MySQL(ip, port)
'''

'''
方式一: @classmethod  ---> 通过类方法来实现单例
'''


class Foo(object):
    # 定义了一个类的数据属性,
    # 用于接收对象的实例，判断对象的实例是否只有一个
    _instance = None  # obj1

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def singleton(cls, *args, **kwargs):
        # 判断类属性_instance是否有值，有代表已经有实例对象
        # 没有则代表没有实例对象，则调用object的__init__获取实例对象
        if not cls._instance:
            # object.__new__(cls): 创造对象
            # 没有参数情况下
            # cls._instance = object.__new__(cls, *args, **kwargs)

            # 有参数的情况下
            cls._instance = cls(*args, **kwargs)  # Foo()

        # 将已经产生的实例对象  直接返回
        return cls._instance


obj1 = Foo.singleton('tank', '123')
obj2 = Foo.singleton('tank', '123')
# print(obj1 is obj2)

'''
方式二: 元类
'''


class MyMeta(type):

    # 1、先触发元类里面的__init__
    def __init__(self, name, base, attrs):  # self --> Goo
        # *** 造空的对象, 然后赋值给了Goo类中的_instance类属性
        self._instance = object.__new__(self)
        # 将类名、基类、类的名称空间，传给type里面的__init__
        super().__init__(name, base, attrs)
        # type.__init__(self, name, base, attrs)

    # 2、当调用Goo类时，等同于调用了由元类实例化的到的对象
    def __call__(self, *args, **kwargs):
        # 判断调用Goo时是否传参
        if args or kwargs:
            init_args = args
            init_kwargs = kwargs

            # 1)通过判断限制了用于传入的参数必须一致，然后返回同一个对象实例
            if init_args == args and init_kwargs == kwargs:
                return self._instance

            # 2) 若不是同一个实例，则新建一个对象，产生新的内存地址
            obj = object.__new__(self)
            self.__init__(obj, *args, **kwargs)
            return obj

        return self._instance


class Goo(metaclass=MyMeta):  # Goo = MyMeta(Goo)
    # _instance = obj
    def __init__(self, x):
        self.x = x


g1 = Goo('1')
g2 = Goo('1')
# print(g1 is g2)  # True

'''
方式三: __new__实现   ---> 通过调用类方法实例化对象时，自动触发的__new__来实现单例
'''


class Aoo(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance


a1 = Aoo()
a2 = Aoo()
# print(a1 is a2)  # True

'''
方式四: 装饰器实现     ---> 通过调用类方法实例化对象时，自动触发的__new__来实现单例
'''


# 单例装饰器
def singleton_wrapper(cls):  # cls ---> Too
    # 因为装饰器可以给多个类使用，所以这里采用字典
    # 以类作为key, 实例对象作为value值
    _instance = {
        # 伪代码: 'Too': Too的示例对象
    }

    def inner(*args, **kwargs):
        # 若当前装饰的类不在字典中，则实例化新类
        # 判断当前装饰的Too类是否在字典中
        if cls not in _instance:
            # obj = cls(*args, **kwargs)
            # return obj
            # 不在，则给字典添加 key为Too， value为Too()---> 实例对象
            # {Too: Too(*args, **kwargs)}
            _instance[cls] = cls(*args, **kwargs)

        # return 对应的实例对象cls(*args, **kwargs)
        return _instance[cls]

    return inner


@singleton_wrapper  # singleton_wrapper(Too)
class Too(object):
    pass


t1 = Too()
t2 = Too()
# print(t1 is t2)  # True

'''
方式五: 模块导入实现
'''
import cls_singleton

s1 = cls_singleton.instance
s2 = cls_singleton.instance

print(s1 is s2)  # True
