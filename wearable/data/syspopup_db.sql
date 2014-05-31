PRAGMA journal_mode = PERSIST;

/* prio : 0~2 (0:low, 2:high) */
/* focus : 0~1 (0:focus, 1:unfocus) */
/* timeout : -1 ~ integer value (-1:infinite, 0:don't use) */
/* term_act : 0~2(0:TERM, 1:HIDE, 2:IGNORE) */
/* endkey_act : 0~2(0:TERM, 1:HIDE, 2:IGNORE) */
CREATE TABLE IF NOT EXISTS syspopup_info (
	id INTEGER PRIMARY KEY,
	name TEXT UNIQUE NOT NULL,
	prio INTEGER,
	focus INTEGER,
	timeout INTEGER,
	term_act INTEGER,
	endkey_act INTEGER,
	pkgname TEXT
);

INSERT OR REPLACE INTO "syspopup_info" VALUES(NULL,"volume",                    1,1,-1,1,1,"com.samsung.windicator");
INSERT OR REPLACE INTO "syspopup_info" VALUES(NULL,"bt-syspopup",		0,0,-1,0,0,"org.tizen.bt-syspopup");
INSERT OR REPLACE INTO "syspopup_info" VALUES(NULL,"poweroff-syspopup",		2,0,-1,0,0,"org.tizen.poweroff-syspopup");
INSERT OR REPLACE INTO "syspopup_info" VALUES(NULL,"lowmem-syspopup",		0,0,5,0,0,"org.tizen.lowmem-syspopup");
INSERT OR REPLACE INTO "syspopup_info" VALUES(NULL,"lowbat-syspopup",		1,0,5,0,0,"org.tizen.lowbat-syspopup");
INSERT OR REPLACE INTO "syspopup_info" VALUES(NULL,"safetyvolume-syspopup",	1,1,-1,0,0,"com.samsung.safetyvolume-syspopup");
INSERT OR REPLACE INTO "syspopup_info" VALUES(NULL,"crash-popup",			1,0,-1,0,0,"org.tizen.crash-popup");
INSERT OR REPLACE INTO "syspopup_info" VALUES(NULL,"fota-syspopup",			2,0,3,0,0,"com.samsung.fota-syspopup");