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


/**

 *
 * @ingroup   SLP_PG
 * @defgroup   SYSPOPUP System Popup

@par SYSPOPUP Programming Guide

<h1 class="pg"> Introduction</h1>
SYSPOPPUP is designed to create popups for system events like low battery, low memory, incoming call etc. Sys-popup (System Popup) Library provides API's for creating system popup applications and launching/destroying the system popup's.
<h1 class="pg"> Scope</h1>
The purpose of this document is to describe how applications can use System Popup Library APIs.\n
This document gives only programming guidelines to system popup application engineers.
The scope of this document is limited to System Popup API usage.

<h1 class="pg"> Syspopup Features</h1>
Syspopup exposes two kinds of API's.
1. Create system popup application.\n
2. Launch System popup application.

<h1 class="pg"> Syspopup Architecture</h1>
\image html syspopup_diag.png "Picture 1. Syspopup Process View"
\image rtf syspopup_diag.png "Picture 1. Syspopup Process View"

Whenever system daemon receives system event for which popup is to be created, it calls syspopup launch API with the required popup name (lowbatt, lowmem etc). Syspopup library finds the appropriate syspopup application to be launched based on the popup name. It then calls the AUL API for launching the syspoup application.
The syspopup application calls syspopup's create API for creating the systempopup. Picture 1 above shows the process view of syspopup.

<h1 class="pg">API list and description</h1>
<ul>
        <li>syspopup_create() : Creates System Popup</li>
        <li>syspopup_reset() : Reset the created system popup properties</li>
        <li>syspopup_has_popup() : Checks system popup is created and is running</li>
	<li>syspopup_launch() : Launches system popup application</li>
	<li>syspopup_destroy_all() : Destroy all the system popups</li>
</ul>
@}
*/

