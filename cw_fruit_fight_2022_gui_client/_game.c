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