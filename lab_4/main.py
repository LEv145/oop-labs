from observer import MyPropertyChangedListener, MeowNotifyDataChanged
from validation import MyPropertyChangingListener, MeowNotifyDataChanging


def main() -> None:
    print("=== Наблюдатель ===")
    meow = MeowNotifyDataChanged()
    meow.add_property_changed_listener(MyPropertyChangedListener(" Офигеть!11!1"))
    meow.add_property_changed_listener(MyPropertyChangedListener(" Ого!"))
    meow.cat = "The dog"
    meow.dog = 42

    print("=== Валидатор ===")
    meow = MeowNotifyDataChanging()
    meow.add_property_changed_listener(MyPropertyChangingListener())
    print("До:   ", meow.cat)
    meow.cat = "The dog"
    print("После:", meow.cat)
    print("До:   ", meow.dog)
    meow.dog = 42
    print("После:", meow.dog)


if __name__ == "__main__":
    main()
