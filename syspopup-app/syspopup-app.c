/*
 * syspopup
 *
 * Copyright (c) 2000 - 2011 Samsung Electronics Co., Ltd. All rights reserved.
 *
 * Contact: Jayoun Lee <airjany@samsung.com>, Sewook Park <sewook7.park@samsung.com>,
 * Jaeho Lee <jaeho81.lee@samsung.com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

#include <tizen.h>
#include <dlog.h>
#include "syspopup.h"
#include "syspopup-app.h"

typedef struct appdata {
	Evas_Object *win;
	Evas_Object *conform;
	Evas_Object *label;
	Evas_Object *popup;
	bundle *b;
	char title[TITLE_BUF_LEN];
	char content[CONTENT_BUF_LEN];
} appdata_s;

int myterm(bundle *b, void *data)
{
	dlog_print(DLOG_DEBUG, LOG_TAG, "myterm called");
	return 0;
}

int mytimeout(bundle *b, void* data)
{
	dlog_print(DLOG_DEBUG, LOG_TAG, "mytimeout called");
	return 0;
}

syspopup_handler handler = {
	.def_term_fn = myterm,
	.def_timeout_fn = mytimeout
};

static bool _app_control_extra_data_cb(app_control_h app_control, const char *key, void *user_data)
{
	int ret;
	char *value;
	appdata_s *ad = user_data;

	ret = app_control_get_extra_data(app_control, key, &value);
	if (ret != APP_CONTROL_ERROR_NONE)
	{
		dlog_print(DLOG_ERROR, LOG_TAG, "app_control_get_extra_data() is failed. err = %d", ret);
	}

	if (bundle_add(ad->b, key, value) != BUNDLE_ERROR_NONE) {
		free(value);
		return APP_CONTROL_ERROR_INVALID_PARAMETER;
	}

	free(value);

	return true;
}

static void win_delete_request_cb(void *data , Evas_Object *obj , void *event_info)
{
	ui_app_exit();
}

static void win_back_cb(void *data, Evas_Object *obj, void *event_info)
{
	appdata_s *ad = data;
	/*  Let window go to hide state. */
	elm_win_lower(ad->win);
}

static void response_cb(void *data, Evas_Object * obj, void *event_info)
{
	dlog_print(DLOG_DEBUG, LOG_TAG, "response_cb called");

	if ((int)event_info != 5)
		evas_object_del(obj);
	elm_exit();
}

static void block_clicked_cb(void *data, Evas_Object *obj, void *event_info)
{
	dlog_print(DLOG_DEBUG, LOG_TAG, "block_clicked_cb called");
	evas_object_del(obj);
}

static void create_base_gui(appdata_s *ad) {

	int w;
	int h;

	ad->win = elm_win_add(NULL, PACKAGE, ELM_WIN_DIALOG_BASIC);
	if (ad->win) {
		elm_win_title_set(ad->win, PACKAGE);
		elm_win_borderless_set(ad->win, EINA_TRUE);
		elm_win_alpha_set(ad->win, EINA_TRUE);
		ecore_x_window_size_get(ecore_x_window_root_first_get(), &w, &h);
		evas_object_resize(ad->win, w, h);
	}

	elm_win_autodel_set(ad->win, EINA_TRUE);
	evas_object_smart_callback_add(ad->win, "delete,request", win_delete_request_cb, NULL);

}

static bool app_create(void *data)
{
	appdata_s *ad = data;

	create_base_gui(ad);

	return true;
}

static void app_control(app_control_h app_control, void *data)
{
	/*  Handle the launch request. */
	appdata_s *ad = data;

	Evas_Object *popup;
	const char *val;
	int ret = 0;

	if(ad->b == NULL)
		ad->b = bundle_create();

	ret = app_control_foreach_extra_data(app_control, _app_control_extra_data_cb, data);
	if (ret != APP_CONTROL_ERROR_NONE)
		dlog_print(DLOG_ERROR, LOG_TAG, "app_control_foreach_extra_data() is failed. err = %d", ret);

	if (syspopup_has_popup(ad->b)) {
		syspopup_reset(ad->b);
	} else {
		popup = elm_popup_add(ad->win);
		if (popup != NULL) {
			ret = syspopup_create(ad->b, &handler, ad->win, ad);
			evas_object_show(ad->win);

			if (ret == 0) {
				val = bundle_get_val(ad->b, "_SYSPOPUP_TITLE_");
				if (val) {
					snprintf(ad->title, TITLE_BUF_LEN, "%s",
							val);
				} else {
					snprintf(ad->title, TITLE_BUF_LEN, "%s",
							"Unknown Title");
				}

				val = bundle_get_val(ad->b, "_SYSPOPUP_CONTENT_");
				if (val) {
					snprintf(ad->content, CONTENT_BUF_LEN,
							"%s", val);
				} else {
					snprintf(ad->content, CONTENT_BUF_LEN,
							"%s", "Unknown Content");
				}

				elm_object_style_set(popup, "char_wrap_style");
				evas_object_size_hint_weight_set(popup,
						EVAS_HINT_EXPAND,
						EVAS_HINT_EXPAND);
				evas_object_smart_callback_add(popup, "block,clicked", block_clicked_cb, NULL);
				elm_object_part_text_set(popup, "title,text", ad->title);
				elm_object_text_set(popup, ad->content);
				evas_object_smart_callback_add(popup,
						"response",
						response_cb,
						NULL);

				evas_object_show(popup);
			}
		}
	}
	bundle_free(ad->b);
}

static void app_pause(void *data)
{
	/*  Take necessary actions when application becomes invisible. */
}

static void app_resume(void *data)
{
	/*  Take necessary actions when application becomes visible. */
}

static void app_terminate(void *data)
{
	/*  Release all resources. */
}

static void ui_app_lang_changed(app_event_info_h event_info, void *user_data)
{
	/* APP_EVENT_LANGUAGE_CHANGED*/
	return;
}

static void ui_app_orient_changed(app_event_info_h event_info, void *user_data)
{
	/* APP_EVENT_DEVICE_ORIENTATION_CHANGED*/
	return;
}

static void ui_app_region_changed(app_event_info_h event_info, void *user_data)
{
	/* APP_EVENT_REGION_FORMAT_CHANGED*/
}

static void ui_app_low_battery(app_event_info_h event_info, void *user_data)
{
	/* APP_EVENT_LOW_BATTERY*/
}

static void ui_app_low_memory(app_event_info_h event_info, void *user_data)
{
	/* APP_EVENT_LOW_MEMORY*/
}

int main(int argc, char *argv[])
{
	appdata_s ad = {0,};
	int ret = 0;

	ui_app_lifecycle_callback_s event_callback = {0,};
	app_event_handler_h handlers[5] = {NULL, };

	event_callback.create = app_create;
	event_callback.terminate = app_terminate;
	event_callback.pause = app_pause;
	event_callback.resume = app_resume;
	event_callback.app_control = app_control;

	ui_app_add_event_handler(&handlers[APP_EVENT_LOW_BATTERY], APP_EVENT_LOW_BATTERY, ui_app_low_battery, &ad);
	ui_app_add_event_handler(&handlers[APP_EVENT_LOW_MEMORY], APP_EVENT_LOW_MEMORY, ui_app_low_memory, &ad);
	ui_app_add_event_handler(&handlers[APP_EVENT_DEVICE_ORIENTATION_CHANGED], APP_EVENT_DEVICE_ORIENTATION_CHANGED, ui_app_orient_changed, &ad);
	ui_app_add_event_handler(&handlers[APP_EVENT_LANGUAGE_CHANGED], APP_EVENT_LANGUAGE_CHANGED, ui_app_lang_changed, &ad);
	ui_app_add_event_handler(&handlers[APP_EVENT_REGION_FORMAT_CHANGED], APP_EVENT_REGION_FORMAT_CHANGED, ui_app_region_changed, &ad);

	ret = ui_app_main(argc, argv, &event_callback, &ad);
	if (ret != APP_ERROR_NONE) {
		dlog_print(DLOG_ERROR, LOG_TAG, "app_main() is failed. err = %d", ret);
	}

	return ret;
}

