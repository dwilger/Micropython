#include "py/runtime.h"
#include "EPD_7in3f.h"
#include "DEV_Config.h"

// Python: photopainter.init()
STATIC mp_obj_t pp_init(void) {
    if (DEV_Module_Init()!= 0) {
        mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("Hardware Init Failed"));
    }
    EPD_7in3f_Init();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(pp_init_obj, pp_init);

// Python: photopainter.display(buffer)
STATIC mp_obj_t pp_display(mp_obj_t image_buffer) {
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(image_buffer, &bufinfo, MP_BUFFER_READ);
    
    // Validate size: 800x480, 4-bit (0.5 byte/pixel) = 192,000 bytes
    if (bufinfo.len < 192000) {
        mp_raise_ValueError(MP_ERROR_TEXT("Buffer too small"));
    }

    EPD_7in3f_Display((uint8_t*)bufinfo.buf);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(pp_display_obj, pp_display);

// Register Module
STATIC const mp_rom_map_elem_t photopainter_globals_table = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_photopainter) },
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&pp_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_display), MP_ROM_PTR(&pp_display_obj) },
};
STATIC MP_DEFINE_CONST_DICT(photopainter_globals, photopainter_globals_table);

const mp_obj_module_t photopainter_user_cmodule = {
   .base = { &mp_type_module },
   .globals = (mp_obj_dict_t*)&photopainter_globals,
};

MP_REGISTER_MODULE(MP_QSTR_photopainter, photopainter_user_cmodule);
