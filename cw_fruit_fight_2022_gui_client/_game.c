#include <Python.h>
#include <structmember.h>

typedef struct Cwff2022gcFruit_Object {
    PyObject_HEAD
    char const *const name;
    PyObject *emoji;
    PyObject *renderer;
} Cwff2022gcFruit_Object;

static PyObject *Cwff2022gcFruit_Repr(Cwff2022gcFruit_Object *self)
{
    return PyUnicode_FromFormat("<fruit '%s'>", self->name);
}

static void Cwff2022gcFruit_Dealloc(Cwff2022gcFruit_Object *self)
{}

static PyMemberDef Cwff2022gcFruit_Members[] = {
    {"__name__", T_STRING, offsetof(Cwff2022gcFruit_Object, name), READONLY, "Name of the fruit"},
    {"emoji", T_OBJECT_EX, offsetof(Cwff2022gcFruit_Object, emoji), READONLY, "Emoji of the fruit"},
    {"renderer", T_OBJECT_EX, offsetof(Cwff2022gcFruit_Object, renderer), READONLY, "Qt renderer bounded with image of the fruit"},
    {NULL}
};

static PyTypeObject Cwff2022gcFruit_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_basicsize = sizeof(Cwff2022gcFruit_Object),
    .tp_name = "cw_fruit_fight_2022_gui_client.game.Cwff2022gcFruit",
    .tp_repr = (reprfunc) Cwff2022gcFruit_Repr,
    .tp_dealloc = (destructor) Cwff2022gcFruit_Dealloc,
    .tp_members = Cwff2022gcFruit_Members
};


static Cwff2022gcFruit_Object Cwff2022gcFruit_Fruits[7] = {
    {
        PyObject_HEAD_INIT(&Cwff2022gcFruit_Type)
        "apple",
        NULL,
        NULL
    },
    {
        PyObject_HEAD_INIT(&Cwff2022gcFruit_Type)
        "banana",
        NULL,
        NULL
    },{
        PyObject_HEAD_INIT(&Cwff2022gcFruit_Type)
        "cherry",
        NULL,
        NULL
    },{
        PyObject_HEAD_INIT(&Cwff2022gcFruit_Type)
        "lemon",
        NULL,
        NULL
    },{
        PyObject_HEAD_INIT(&Cwff2022gcFruit_Type)
        "orange",
        NULL,
        NULL
    },{
        PyObject_HEAD_INIT(&Cwff2022gcFruit_Type)
        "pineapple",
        NULL,
        NULL
    },{
        PyObject_HEAD_INIT(&Cwff2022gcFruit_Type)
        "watermelon",
        NULL,
        NULL
    },
};


Cwff2022gcFruit_Object *const Cwff2022gcFruit_Apple = &(Cwff2022gcFruit_Fruits[0]);
Cwff2022gcFruit_Object *const Cwff2022gcFruit_Banana = &(Cwff2022gcFruit_Fruits[1]);
Cwff2022gcFruit_Object *const Cwff2022gcFruit_Cherry = &(Cwff2022gcFruit_Fruits[2]);
Cwff2022gcFruit_Object *const Cwff2022gcFruit_Lemon = &(Cwff2022gcFruit_Fruits[3]);
Cwff2022gcFruit_Object *const Cwff2022gcFruit_Orange = &(Cwff2022gcFruit_Fruits[4]);
Cwff2022gcFruit_Object *const Cwff2022gcFruit_Pineapple = &(Cwff2022gcFruit_Fruits[5]);
Cwff2022gcFruit_Object *const Cwff2022gcFruit_Watermelon = &(Cwff2022gcFruit_Fruits[6]);

void _Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Object *self, PyObject *value) {
    Py_INCREF(value);
    self->emoji = value;
}

PyObject *_Cwff2022gcFruit_GetEmoji(Cwff2022gcFruit_Object *self) {
    Py_INCREF(self->emoji);
    return self->emoji;
}

void _Cwff2022gcFruit_SetRenderer(Cwff2022gcFruit_Object *self, PyObject *value) {
    Py_INCREF(value);
    self->renderer = value;
}


PyTypeObject * _Cwff2022gcFruit_PrepareType(PyObject *dct) {
    Py_INCREF(dct);
    Cwff2022gcFruit_Type.tp_dict = dct;
    if (PyType_Ready(&Cwff2022gcFruit_Type) != 0)
        return NULL;

    return &Cwff2022gcFruit_Type;
}

typedef struct Cwff2022gcGameState_Object {
    PyObject_HEAD
    int is_ended;
    PyObject *stamina;
    PyObject *players;
    PyObject *table;
    PyObject *buttons;
} Cwff2022gcGameState_Object;


int _Cwff2022gcGameState_New(
    PyObject *raw_text,
    PyObject *buttons_in,
    int *is_ended,
    PyObject **stamina,
    PyObject **players,
    PyObject **table,
    PyObject **buttons_out
);

static Cwff2022gcGameState_Object *Cwff2022gcGameState_New(PyTypeObject *cls, PyObject *args, PyObject *kwargs) {
    static char const* const kw_names[] = {"raw_text", "buttons", NULL};
    PyObject *raw_text;
    PyObject *buttons;
    Cwff2022gcGameState_Object *self;
    Cwff2022gcGameState_Object data;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", kw_names, &raw_text, &buttons))
    { return NULL; }

    switch (_Cwff2022gcGameState_New(raw_text, buttons, &(data.is_ended), &(data.stamina), &(data.players), &(data.table), &(data.buttons)))
    {
        case -1:
            return NULL;
        case 0:
            Py_RETURN_NONE;
        case 1:
            break;
        default:
            Py_UNREACHABLE();
    }
    self = cls->tp_alloc(cls, 0);
    if (self == NULL)
    {
        Py_DECREF(data.stamina);
        Py_DECREF(data.players);
        Py_DECREF(data.table);
        Py_XDECREF(data.buttons);
        return PyErr_NoMemory();
    }

    self->is_ended = data.is_ended;
    self->stamina = data.stamina;
    self->players = data.players;
    self->table = data.table;
    self->buttons = data.buttons;

    return self;
}

/*
static PyObject *Cwff2022gcGameState_Repr(Cwff2022gcGameState_Object *self)
{
    return PyUnicode_FromFormat("<player name='%U'>", self->name);
}
*/

static void Cwff2022gcGameState_Dealloc(Cwff2022gcGameState_Object *self)
{
    Py_DECREF(self->stamina);
    Py_DECREF(self->players);
    Py_DECREF(self->table);
    Py_XDECREF(self->buttons);
    Py_TYPE(self)->tp_free(self);
}

static PyMemberDef Cwff2022gcGameState_Members[] = {
    {"is_ended", T_BOOL, offsetof(Cwff2022gcGameState_Object, is_ended), READONLY, "Is game ended or can be continued"},
    {"stamina", T_OBJECT_EX, offsetof(Cwff2022gcGameState_Object, stamina), READONLY, "Game stamina"},
    {"players", T_OBJECT_EX, offsetof(Cwff2022gcGameState_Object, players), READONLY, "Participants of game"},
    {"table", T_OBJECT_EX, offsetof(Cwff2022gcGameState_Object, table), READONLY, "Current bones on table (fruits on end of chain)"},
    {"buttons", T_OBJECT, offsetof(Cwff2022gcGameState_Object, buttons), READONLY, "Buttons with move variants"},
    {NULL}
};

static PyTypeObject Cwff2022gcGameState_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_basicsize = sizeof(Cwff2022gcGameState_Object),
    .tp_name = "cw_fruit_fight_2022_gui_client.game.Cwff2022gcGameState",
    .tp_new = Cwff2022gcGameState_New,
    // .tp_repr = (reprfunc) Cwff2022gcGameState_Repr,
    .tp_dealloc = (destructor) Cwff2022gcGameState_Dealloc,
    .tp_members = Cwff2022gcGameState_Members
};

PyTypeObject * _Cwff2022gcGameState_PrepareType(PyObject *dct) {
    Py_INCREF(dct);
    Cwff2022gcGameState_Type.tp_dict = dct;
    if (PyType_Ready(&Cwff2022gcGameState_Type) != 0)
        return NULL;

    return &Cwff2022gcGameState_Type;
}