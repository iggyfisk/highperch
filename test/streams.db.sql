BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Twitch" (
	"TwitchID"	INTEGER NOT NULL UNIQUE,
	"Streaming"	INTEGER NOT NULL DEFAULT 0,
	"Name"	TEXT,
	"URL"	TEXT,
	"Game"	TEXT,
	"Status"	TEXT,
	PRIMARY KEY("TwitchID")
);
INSERT INTO "Twitch" VALUES (9637278,0,NULL,NULL,NULL,NULL);
INSERT INTO "Twitch" VALUES (10584456,0,NULL,NULL,NULL,NULL);
INSERT INTO "Twitch" VALUES (19152680,0,NULL,NULL,NULL,NULL);
INSERT INTO "Twitch" VALUES (42016697,0,NULL,NULL,NULL,NULL);
INSERT INTO "Twitch" VALUES (48136754,0,NULL,NULL,NULL,NULL);
INSERT INTO "Twitch" VALUES (325318767,0,NULL,NULL,NULL,NULL);
COMMIT;
