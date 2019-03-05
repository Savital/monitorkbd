# lkm keymonitoring.c

https://github.com/torvalds/linux/blob/08b5fa819970c318e58ab638f497633c25971813/drivers/input/keyboard/xtkbd.c

 3 keys states:
 * down = 0
 * pressed = 1
 * up = 2
 
keyboard layouts:
 * EN (lower, upper) = (0, 1)
 * RU (lower, upper) = (2, 3)
 
```bash
struct keystore_item 
{
    int id;
	int state;
	int scancode;
    int layout;
	unsigned long long downtime;
	unsigned long long searchtime;
	struct keystore_item *next;
}
```

msg - message buffer contains keystore_item data

keystore - hash table contains keys data and state for keyboard

log_queue_table - table contains 

IRQF_SHARED — разрешить разделение (совместное использование) линии IRQ с другими PCI устройствами;

#define ENOMEM 12 / * Недостаточно памяти * /

WQ_MEM_RECLAIM | WQ_HIGHPRI //TODO ???

## Клавиатура (свойства)
 * раскладка клавиатуры;
 * скорость повтора посылаемых клавиатурой сигналов в случае удержания клавиш пользователем;
 * длительность интервала задержки от момента нажатия клавиши до того момента, когда клавиатура начинает повторять посылку сигналов.
 
 
 Скрипт отображает информацию обо всех устройствах ввода присутствующих в системе
 ```bash
 cat /proc/bus/input/devices
 ```