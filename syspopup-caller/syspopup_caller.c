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


#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <glib.h>
#include <gio/gio.h>
#include <aul.h>
#include <vasum.h>
#include <appsvc.h>
#include <system_info.h>

#include "syspopup_core.h"
#include "syspopup_db.h"
#include "syspopup_api.h"
#include "simple_util.h"

static int __initialized = 0;
static bool __zone_armed = 0;

#define TIZEN_ZONE_CONFIG_KEY "tizen.org/feature/container"

API int syspopup_launch(char *popup_name, bundle *b)
{
	syspopup_info_t *info = NULL;
	int ret;
	int is_bundle = 0;
	vsm_context_h vsm_ctx = NULL;
	vsm_zone_h fg_zone = NULL;
	const char *fg_zone_name = NULL;

	if (popup_name == NULL) {
		_E("popup_name is NULL");
		return -1;
	}

	if (!__initialized) {
		ret = system_info_get_platform_bool(TIZEN_ZONE_CONFIG_KEY, &__zone_armed);
		if (ret != SYSTEM_INFO_ERROR_NONE) {
			_E("failed to get zone status, set zone status to disarmed");
			__zone_armed = 0;
		}
		__initialized = 1;
	}

	info = _syspopup_info_get(popup_name);
	if (info == NULL || info->pkgname == NULL) {
		_E("info or info->pkgname is NULL");
		if (info)
			_syspopup_info_free(info);
		return -1;
	}

	if (b == NULL) {
		b = bundle_create();
		is_bundle = 1;
	}

	if (_syspopup_set_name_to_bundle(b, popup_name) < 0) {
		_E("bundle set error");
		_syspopup_info_free(info);

		if (is_bundle == 1) {
			bundle_free(b);
		}
		return -1;
	}

	if (__zone_armed) {
		if (vsm_is_virtualized()) {
			ret = aul_launch_app(info->pkgname, b);
			if (ret < 0)
				_E("aul launch error - %d", ret);

			goto out;
		}
#if !GLIB_CHECK_VERSION(2, 35, 0)
		g_type_init();
#endif
		vsm_ctx = vsm_create_context();
		if (vsm_ctx) {
			fg_zone = vsm_get_foreground(vsm_ctx);
			if (fg_zone == NULL) {
				_E("failed to get foreground zone");
				ret = -1;
				goto out;
			}

			if (vsm_is_host_zone(fg_zone) == 1) {
				_E("can not launch syspopup. foreground zone is host");
				ret = -1;
				goto out;
			}

			fg_zone_name = vsm_get_zone_name(fg_zone);
			_D("foreground zone: %s", fg_zone_name);
		} else {
			_E("failed to create vsm_context");
			ret = -1;
			goto out;
		}

		if (fg_zone_name) {
			appsvc_set_operation(b, APP_SVC_OPERATION_JUMP);
			appsvc_add_data(b, APP_SVC_K_JUMP_ORIGIN_OPERATION, APPSVC_OPERATION_DEFAULT);
			appsvc_add_data(b, APP_SVC_K_JUMP_ZONE_NAME, fg_zone_name);
			appsvc_set_appid(b, info->pkgname);
			ret = appsvc_run_service(b, 0, NULL, NULL);
			if (ret < 0) {
				_E("syspopup launch error - %d", ret);
			}
		} else {
			_E("failed to get foreground zone name");
			ret = -1;
			goto out;
		}

	}
	else {
		ret = aul_launch_app(info->pkgname, b);
		if (ret < 0)
			_E("aul launch error - %d", ret);

		goto out;
	}

out:
	if (vsm_ctx) {
		vsm_cleanup_context(vsm_ctx);
	}

	if (is_bundle == 1) {
		bundle_free(b);
	}

	_syspopup_info_free(info);

	return ret;
}

API int syspopup_destroy_all()
{
	GDBusConnection *conn = NULL;
	GError *err = NULL;
	int ret = 0;

	g_type_init();

	conn = g_bus_get_sync(G_BUS_TYPE_SYSTEM,NULL,&err);

	if (err) {
		_E("gdbus connection error (%s)", err->message);
		ret = -1;
		goto out;
	}
	if (NULL == conn) {
		_E("gdbus connection is not set, even gdbus error isn't raised");
		ret = -1;
		goto out;
	}

	if(!g_dbus_connection_emit_signal(conn,NULL,
						SYSPOPUP_DBUS_PATH,
						SYSPOPUP_DBUS_SIGNAL_INTERFACE,
						SYSPOPUP_DBUS_SP_TERM_SIGNAL,
						NULL,
						&err)) {
		_E("Error emitting the signal: %s",err->message);
		ret = -1;
		goto out;
	}

out :
	_D("send signal done\n");
	if (err) {
		g_error_free(err);
		err = NULL;
	}

	if (conn) {
		g_object_unref(conn);
		conn = NULL;
	}

	return ret;
}

