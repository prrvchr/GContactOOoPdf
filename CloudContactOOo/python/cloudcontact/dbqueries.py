#!
# -*- coding: utf_8 -*-

from com.sun.star.logging.LogLevel import INFO
from com.sun.star.logging.LogLevel import SEVERE

from .dbconfig import g_csv
from .configuration import g_member

from .logger import logMessage
from .logger import getMessage


def getSqlQuery(ctx, name, format=None):

# Create Text Table Queries
    if name == 'createTableTables':
        c1 = '"Table" INTEGER NOT NULL PRIMARY KEY'
        c2 = '"Name" VARCHAR(100) NOT NULL'
        c3 = '"Identity" INTEGER DEFAULT NULL'
        c4 = '"View" BOOLEAN DEFAULT TRUE'
        c5 = '"Versioned" BOOLEAN DEFAULT FALSE'
        k1 = 'CONSTRAINT "UniqueTablesName" UNIQUE("Name")'
        c = (c1, c2, c3, c4, c5, k1)
        query = 'CREATE TEXT TABLE "Tables"(%s)' % ','.join(c)

    elif name == 'createTableColumns':
        c1 = '"Column" INTEGER NOT NULL PRIMARY KEY'
        c2 = '"Name" VARCHAR(100) NOT NULL'
        k1 = 'CONSTRAINT "UniqueColumnsName" UNIQUE("Name")'
        c = (c1, c2, k1)
        query = 'CREATE TEXT TABLE "Columns"(%s)' % ','.join(c)

    elif name == 'createTableTableColumn':
        c1 = '"Table" INTEGER NOT NULL'
        c2 = '"Column" INTEGER NOT NULL'
        c3 = '"TypeName" VARCHAR(100) NOT NULL'
        c4 = '"TypeLenght" SMALLINT DEFAULT NULL'
        c5 = '"Default" VARCHAR(100) DEFAULT NULL'
        c6 = '"Options" VARCHAR(100) DEFAULT NULL'
        c7 = '"Primary" BOOLEAN NOT NULL'
        c8 = '"Unique" BOOLEAN NOT NULL'
        c9 = '"ForeignTable" INTEGER DEFAULT NULL'
        c10 = '"ForeignColumn" INTEGER DEFAULT NULL'
        k1 = 'PRIMARY KEY("Table","Column")'
        k2 = 'CONSTRAINT "ForeignTableColumnTable" FOREIGN KEY("Table") REFERENCES '
        k2 += '"Tables"("Table") ON DELETE CASCADE ON UPDATE CASCADE'
        k3 = 'CONSTRAINT "ForeignTableColumnColumn" FOREIGN KEY("Column") REFERENCES '
        k3 += '"Columns"("Column") ON DELETE CASCADE ON UPDATE CASCADE'
        c = (c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, k1, k2, k3)
        query = 'CREATE TEXT TABLE "TableColumn"(%s)' % ','.join(c)

    elif name == 'createTableSettings':
        c1 = '"Setting" INTEGER NOT NULL PRIMARY KEY'
        c2 = '"Name" VARCHAR(100) NOT NULL'
        c3 = '"Value1" VARCHAR(100) NOT NULL'
        c4 = '"Value2" VARCHAR(100) DEFAULT NULL'
        c5 = '"Value3" VARCHAR(100) DEFAULT NULL'
        k1 = 'CONSTRAINT "UniqueSettingsName" UNIQUE("Name")'
        c = (c1, c2, c3, c4, c5, k1)
        p = ','.join(c)
        query = 'CREATE TEXT TABLE "Settings"(%s)' % p

    elif name == 'createTableTypes':
        c1 = '"Type" INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY'
        c2 = '"Name" VARCHAR(100) NOT NULL'
        c3 = '"Value" VARCHAR(100) NOT NULL'
        c4 = '"Custom" BOOLEAN DEFAULT TRUE NOT NULL'
        k1 = 'CONSTRAINT "UniqueTypesValue" UNIQUE("Value")'
        c = (c1, c2, c3, c4, k1)
        query = 'CREATE TEXT TABLE "Types"(%s)' % ','.join(c)

    elif name == 'createTableTableType':
        c1 = '"Table" INTEGER NOT NULL'
        c2 = '"Type" INTEGER NOT NULL'
        c3 = '"Default" BOOLEAN DEFAULT NULL'
        k1 = 'PRIMARY KEY("Table","Type")'
        #k2 = 'CONSTRAINT "UniqueTypesDefault" UNIQUE("Table","Default")'
        k2 = 'CONSTRAINT "ForeignTableTypeTable" FOREIGN KEY("Table") REFERENCES '
        k2 += '"Tables"("Table") ON DELETE CASCADE ON UPDATE CASCADE'
        k3 = 'CONSTRAINT "ForeignTableTypeType" FOREIGN KEY("Type") REFERENCES '
        k3 += '"Types"("Type") ON DELETE CASCADE ON UPDATE CASCADE'
        c = (c1, c2, c3, k1, k2, k3)
        query = 'CREATE TEXT TABLE "TableType"(%s)' % ','.join(c)

    elif name == 'createTableLabels':
        c1 = '"Label" INTEGER NOT NULL PRIMARY KEY'
        c2 = '"Name" VARCHAR(100) NOT NULL'
        k1 = 'CONSTRAINT "UniqueLabelsName" UNIQUE("Name")'
        c = (c1, c2, k1)
        p = ','.join(c)
        query = 'CREATE TEXT TABLE "Labels"(%s)' % p

    elif name == 'createTableTableLabel':
        c1 = '"Table" INTEGER NOT NULL'
        c2 = '"Label" INTEGER NOT NULL'
        c3 = '"View" VARCHAR(10) DEFAULT NULL'
        k1 = 'PRIMARY KEY("Table","Label")'
        k2 = 'CONSTRAINT "UniqueTableLabelView" UNIQUE("View")'
        k3 = 'CONSTRAINT "ForeignTableLabelTable" FOREIGN KEY("Table") REFERENCES '
        k3 += '"Tables"("Table") ON DELETE CASCADE ON UPDATE CASCADE'
        k4 = 'CONSTRAINT "ForeignTableLabelLabel" FOREIGN KEY("Label") REFERENCES '
        k4 += '"Labels"("Label") ON DELETE CASCADE ON UPDATE CASCADE'
        c = (c1, c2, c3, k1, k2, k3, k4)
        query = 'CREATE TEXT TABLE "TableLabel"(%s)' % ','.join(c)

    elif name == 'createTableFields':
        c1 = '"Field" INTEGER NOT NULL PRIMARY KEY'
        c2 = '"Method" VARCHAR(100) NOT NULL'
        c3 = '"Name" VARCHAR(100) NOT NULL'
        c4 = '"Type" VARCHAR(100) NOT NULL'
        c5 = '"Table" VARCHAR(100) NOT NULL'
        c6 = '"Column" INTEGER NOT NULL'
        k1 = 'CONSTRAINT "UniqueFieldsName" UNIQUE("Method", "Name")'
        c = (c1, c2, c3, c4, c5, c6, k1)
        p = ','.join(c)
        query = 'CREATE TEXT TABLE "Fields"(%s)' % p

    elif name == 'setTableSource':
        query = 'SET TABLE "%s" SOURCE "%s"' % (format, g_csv % format)

    elif name == 'setTableHeader':
        query = 'SET TABLE "%s" SOURCE HEADER "%s"' % format

    elif name == 'setTableReadOnly':
        query = 'SET TABLE "%s" READONLY TRUE' % format

# Create Cached Table Options
    elif name == 'getPrimayKey':
        query = 'PRIMARY KEY(%s)' % ','.join(format)

    elif name == 'getUniqueConstraint':
        query = 'CONSTRAINT "Unique%(Table)s%(Column)s" UNIQUE("%(Column)s")' % format

    elif name == 'getForeignConstraint':
        q = 'CONSTRAINT "Foreign%(Table)s%(Column)s" FOREIGN KEY("%(Column)s") REFERENCES '
        q += '"%(ForeignTable)s"("%(ForeignColumn)s") ON DELETE CASCADE ON UPDATE CASCADE'
        query = q % format

# Create Cached Table Queries
    elif name == 'createTable':
        query = 'CREATE CACHED TABLE "%s"(%s)' % format

    elif name == 'getPeriodColumns':
        query = '"Start" TIMESTAMP GENERATED ALWAYS AS ROW START,'
        query += '"Stop" TIMESTAMP GENERATED ALWAYS AS ROW END,'
        query += 'PERIOD FOR SYSTEM_TIME("Start","Stop")'

    elif name == 'getSystemVersioning':
        query = ' WITH SYSTEM VERSIONING'

# Create Synonym Queries
    elif name == 'createSynonym':
        query = 'CREATE SYNONYM "PUBLIC"."%(View)s" FOR "%(Schema)s"."%(View)s"' % format

# Create Dynamic View Queries
    elif name == 'createView':
        query = 'CREATE VIEW "%s"(%s) AS SELECT %s FROM %s' % format

    elif name == 'createGroupView':
        q = '''\
CREATE VIEW IF NOT EXISTS "%(View)s" AS
  SELECT "AddressBook".* FROM "AddressBook"
  JOIN "Peoples" ON "AddressBook"."Resource"="Peoples"."Resource"
  JOIN "Connections" ON "Peoples"."People"="Connections"."People"
  JOIN "Groups" ON "Connections"."Group"="Groups"."Group"
  WHERE "Groups"."Group"=%(Group)s ORDER BY "Peoples"."People";
GRANT SELECT ON "%(View)s" TO "%(User)s";
'''
        query = q % format

# Drop Dynamic View Queries
    elif name == 'dropGroupView':
        query = 'DROP VIEW IF EXISTS "%(View)s"' % format

# Create Trigger Query
    elif name == 'createTriggerUpdateAddressBook':
        query = 'CREATE TRIGGER "AddressBookUpdate" INSTEAD OF UPDATE ON "AddressBook" '
        query += 'REFERENCING NEW AS "new" OLD AS "old" FOR EACH ROW BEGIN ATOMIC %s END' % format

    elif name == 'createTriggerUpdateAddressBookCore':
        q = 'IF "new"."%(View)s" <> "old"."%(View)s" THEN '
        q += 'UPDATE "%(Table)s" SET "Value"="new"."%(View)s" WHERE '
        q += '"People"="new"."People" AND "Label"=%(LabelId)s'
        if format['TypeId'] is not None:
            q += ' AND "Type"=%(TypeId)s'
        q += '; END IF;'
        query = q % format

# Create User, Role and Schema Query
    elif name == 'createUser':
        q = 'CREATE USER "%(User)s" PASSWORD \'%(Password)s\''
        if format.get('Admin', False):
            q += ' ADMIN'
        query = q % format

    elif name == 'createRole':
        query = 'CREATE ROLE "%(Role)s"' % format

    elif name == 'setRole':
        query = 'GRANT "%(Role)s" TO "%(User)s"' % format

    elif name == 'createSchema':
        query = 'CREATE SCHEMA "%(User)s" AUTHORIZATION "%(User)s"' % format

    elif name == 'setUserSchema':
        q = 'ALTER USER "%(User)s" SET INITIAL SCHEMA'
        if format.get('Admin', False):
            #q += ' PUBLIC'
            q += ' "%(User)s"'
        else:
            q += ' "%(User)s"'
        query = q % format

# Get last IDENTITY value that was inserted into a table by the current session
    elif name == 'getIdentity':
        query = 'CALL IDENTITY();'

# Get Users and Privileges Query
    elif name == 'getUsers':
        query = 'SELECT * FROM INFORMATION_SCHEMA.SYSTEM_USERS'
    elif name == 'getPrivileges':
        query = 'SELECT * FROM INFORMATION_SCHEMA.TABLE_PRIVILEGES'
    elif name == 'changePassword':
        query = "SET PASSWORD '%s'" % format

# Select Queries
    elif name == 'getTableName':
        query = 'SELECT "Name" FROM "Tables" WHERE "View" IS NOT NULL ORDER BY "Table"'

    elif name == 'getViewName':
        query = 'SELECT "Name" FROM "Tables" WHERE "View"=TRUE ORDER BY "Table"'

    elif name == 'getTables':
        s1 = '"T"."Table" AS "TableId"'
        s2 = '"C"."Column" AS "ColumnId"'
        s3 = '"T"."Name" AS "Table"'
        s4 = '"C"."Name" AS "Column"'
        s5 = '"TC"."TypeName" AS "Type"'
        s6 = '"TC"."TypeLenght" AS "Lenght"'
        s7 = '"TC"."Default"'
        s8 = '"TC"."Options"'
        s9 = '"TC"."Primary"'
        s10 = '"TC"."Unique"'
        s11 = '"TC"."ForeignTable" AS "ForeignTableId"'
        s12 = '"TC"."ForeignColumn" AS "ForeignColumnId"'
        s13 = '"T2"."Name" AS "ForeignTable"'
        s14 = '"C2"."Name" AS "ForeignColumn"'
        s15 = '"T"."View"'
        s16 = '"T"."Versioned"'
        s = (s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16)
        f1 = '"Tables" AS "T"'
        f2 = 'JOIN "TableColumn" AS "TC" ON "T"."Table" = "TC"."Table"'
        f3 = 'JOIN "Columns" AS "C" ON "TC"."Column" = "C"."Column"'
        f4 = 'LEFT JOIN "Tables" AS "T2" ON "TC"."ForeignTable" = "T2"."Table"'
        f5 = 'LEFT JOIN "Columns" AS "C2" ON "TC"."ForeignColumn" = "C2"."Column"'
        w = '"T"."Name" = ?'
        f = (f1, f2, f3, f4, f5)
        p = (', '.join(s), ' '.join(f), w)
        query = 'SELECT %s FROM %s WHERE %s' % p

    elif name == 'getViews':
        s1 = '"T1"."Table" AS "TableId"'
        s2 = '"TL"."Label" AS "LabelId"'
        s3 = '"TT"."Type" AS "TypeId"'
        s4 = '"T1"."Name" AS "Table"'
        s5 = '"L"."Name" AS "Label"'
        s6 = '"T"."Name" AS "Type"'
        s7 = 'CONCAT(COALESCE("T"."Name",\'\'),COALESCE("TL"."View","L"."Name")) AS "View"'
        s8 = '"T2"."Name" AS "PrimaryTable"'
        s9 = '"C"."Name" AS "PrimaryColumn"'
        s = (s1,s2,s3,s4,s5,s6,s7,s8,s9)
        f1 = '"Tables" AS "T1", "Tables" AS "T2"'
        f2 = 'JOIN "TableLabel" AS "TL" ON "T1"."Table"="TL"."Table"'
        f3 = 'JOIN "Labels" AS "L" ON "TL"."Label"="L"."Label"'
        f4 = 'LEFT JOIN "TableType" AS "TT" ON "T1"."Table"="TT"."Table"'
        f5 = 'LEFT JOIN "Types" AS "T" ON "TT"."Type"="T"."Type"'
        f6 = 'JOIN "Columns" AS "C" ON "T2"."Identity"="C"."Column"'
        w = '"T2"."Identity"=1 AND "T1"."Name"=? '
        f = (f1, f2, f3, f4, f5, f6)
        p = (','.join(s), ' '.join(f), w)
        query = 'SELECT %s FROM %s WHERE %s ORDER BY "TableId","LabelId","TypeId"' % p

    elif name == 'getFieldNames':
        s = '"Fields"."Name"'
        f1 = '"Fields"'
        f2 = 'JOIN "Tables" ON "Fields"."Table"=%s AND "Fields"."Column"="Tables"."Table"'
        f = (f1, f2 % "'Tables'")
        w1 = '"Tables"."View"=TRUE'
        w2 = '"Fields"."Table"=%s AND "Fields"."Column"=1' % "'Loop'"
        p = (s, ' '.join(f), w1, s, f1, w2)
        query = 'SELECT %s FROM %s WHERE %s UNION SELECT %s FROM %s WHERE %s' % p

    elif name == 'getFieldsMap':
        s1 = '"F"."Name" AS "Value"'
        s2 = 'COALESCE("Tables"."Name","Columns"."Name","Labels"."Name","Fields"."Name") AS "Name"'
        s3 = '"F"."Type"'
        s4 = '"F"."Table"'
        s = (s1, s2, s3, s4)
        f1 = '"Fields" AS "F"'
        f2 = 'LEFT JOIN "Tables" ON "F"."Table"=%s AND "F"."Column"="Tables"."Table"'
        f3 = 'LEFT JOIN "Columns" ON "F"."Table"=%s AND "F"."Column"="Columns"."Column"'
        f4 = 'LEFT JOIN "Labels" ON "F"."Table"=%s AND "F"."Column"="Labels"."Label"'
        f5 = 'LEFT JOIN "Fields" ON "F"."Table"=%s AND "F"."Field"="Fields"."Field"'
        f = (f1, f2 % "'Tables'", f3 % "'Columns'", f4 % "'Labels'", f5 % "'Loop'")
        p = (','.join(s), ' '.join(f))
        query = 'SELECT %s FROM %s WHERE "F"."Method"=? ORDER BY "F"."Field"' % p

    elif name == 'getPrimaryTable':
        s = 'COALESCE("Tables"."Name","Columns"."Name","Labels"."Name","Fields"."Name") AS "Name"'
        f1 = '"Fields" AS "F"'
        f2 = 'LEFT JOIN "Tables" ON "F"."Table"=%s AND "F"."Column"="Tables"."Table"'
        f3 = 'LEFT JOIN "Columns" ON "F"."Table"=%s AND "F"."Column"="Columns"."Column"'
        f4 = 'LEFT JOIN "Labels" ON "F"."Table"=%s AND "F"."Column"="Labels"."Label"'
        f5 = 'LEFT JOIN "Fields" ON "F"."Table"=%s AND "F"."Field"="Fields"."Field"'
        f = (f1, f2 % "'Tables'", f3 % "'Columns'", f4 % "'Labels'", f5 % "'Loop'")
        w = '"F"."Type"=%s AND "F"."Table"=%s' % ("'Primary'","'Tables'")
        p = (s, ' '.join(f), w)
        query = 'SELECT %s FROM %s WHERE %s' % p

    elif name == 'getPerson':
        c = '"People","Group","Resource","Account","PeopleSync","GroupSync"'
        f = '"Peoples" JOIN "Groups"'
        o1 = '"Peoples"."People"="Groups"."People"'
        o2 = '"Peoples"."Resource"="Groups"."Resource"'
        w = '"Peoples"."Account"=?'
        query = 'SELECT %s FROM %s ON %s AND %s WHERE %s' % (c, f, o1, o2, w)

    elif name == 'getUpdatedGroup':
        query = 'SELECT "Resource" FROM "Groups" FOR SYSTEM_TIME AS OF CURRENT_TIMESTAMP - 1 YEAR'

# Update Queries
    elif name == 'updatePeoples':
        query = 'UPDATE "Peoples" SET "TimeStamp"=? WHERE "Resource"=?'

    elif name == 'updatePeopleSync':
        query = 'UPDATE "Peoples" SET "PeopleSync"=?,"TimeStamp"=? WHERE "People"=?'

    elif name == 'updateGroupSync':
        query = 'UPDATE "Peoples" SET "GroupSync"=?,"TimeStamp"=? WHERE "People"=?'

# Get DataBase Version Query
    elif name == 'getVersion':
        query = 'Select DISTINCT DATABASE_VERSION() as "HSQL Version" From INFORMATION_SCHEMA.SYSTEM_TABLES'

# Create Trigger Query
    elif name == 'createTriggerGroupInsert':
        query = """\
CREATE TRIGGER "GroupInsert" AFTER INSERT ON "Groups"
  REFERENCING NEW ROW AS "NewRow"
  FOR EACH ROW
  BEGIN ATOMIC
    CALL "GroupView" ("NewRow"."Name", "NewRow"."Group")
  END"""

    elif name == 'selectUpdatedGroup':
        c1 = '?||"Resource" AS "Resource"'
        c2 = '"Group"'
        c3 = '"Name"'
        q = '\
SELECT %s FROM "Groups" WHERE "GroupSync"=FALSE AND "People"=? AND "Resource"<>?'
        query = q % ','.join((c1, c2, c3))

    elif name == 'truncatGroup':
        q = """\
TRUNCATE TABLE "Groups" VERSIONING TO TIMESTAMP'%(TimeStamp)s'"""
        query = q % format

# Create Procedure Query
    elif name == 'createSelectGroup':
        query = """\
CREATE PROCEDURE "SelectGroup"(IN "Prefix" VARCHAR(50),
                               IN "PeopleId" INTEGER,
                               IN "ResourceName" VARCHAR(100))
  SPECIFIC "SelectGroup_1"
  READS SQL DATA
  DYNAMIC RESULT SETS 1
  BEGIN ATOMIC
    DECLARE "StartTime","EndTime","Format" VARCHAR(30);
    DECLARE "TmpTime" TIMESTAMP(6);
    DECLARE "Result" CURSOR WITH RETURN FOR
      SELECT "Prefix"||"Resource" FROM "Groups" FOR SYSTEM_TIME FROM 
      TO_TIMESTAMP('%(Start)s','%(Format)s') TO TO_TIMESTAMP('%(End)s','%(Format)s')
      WHERE "People"="PeopleId" AND "Resource"<>"ResourceName" FOR READ ONLY;
    SET "Time" = LOCALTIMESTAMP(6)
    SET "TmpTime" = "Time" - 10 MINUTE
    SET "Format" = 'YYYY-MM-DDTHH24:MI:SS.FFFZ'
    SET "EndTime" = TO_CHAR("Time","Format");
    SET "StartTime" = TO_CHAR("TmpTime","Format");
    SET "Time" = "EndTime";
    OPEN "Result";
  END"""

    elif name == 'createInsertUser':
        query = """\
CREATE PROCEDURE "InsertUser"(IN "ResourceName" VARCHAR(100),
                              IN "UserName" VARCHAR(100),
                              IN "GroupName" VARCHAR(100))
  SPECIFIC "InsertUser_1"
  MODIFIES SQL DATA
  DYNAMIC RESULT SETS 1
  BEGIN ATOMIC
    DECLARE "Result" CURSOR WITH RETURN FOR
      SELECT "People", "Group", "Resource", "Account", "PeopleSync", "GroupSync"
      FROM "Peoples" JOIN "Groups" ON "Peoples"."People"="Groups"."People"
      AND "Peoples"."Resource"="Groups"."Resource"
      WHERE "Peoples"."Resource"="ResourceName" FOR READ ONLY;
    INSERT INTO "Peoples" ("Resource","Account") VALUES ("ResourceName","UserName");
    INSERT INTO "Groups" ("People","Resource","Name")
      VALUES (IDENTITY(),"ResourceName","GroupName");
    OPEN "Result";
  END"""

    elif name == 'createGetPeopleIndex':
        query = """\
CREATE FUNCTION "GetPeopleIndex"("Prefix" VARCHAR(50),"ResourceName" VARCHAR(100))
  RETURNS INTEGER
  SPECIFIC "GetPeopleIndex_1"
  READS SQL DATA
  RETURN (SELECT "People" FROM "Peoples" WHERE "Prefix"||"Resource"="ResourceName");
"""

    elif name == 'createGetLabelIndex':
        query = """\
CREATE FUNCTION "GetLabelIndex"("LabelName" VARCHAR(100))
  RETURNS INTEGER
  SPECIFIC "GetLabelIndex_1"
  READS SQL DATA
  RETURN (SELECT "Label" FROM "Labels" WHERE "Name"="LabelName");
"""

    elif name == 'createGetTypeIndex':
        query = """\
CREATE PROCEDURE "GetTypeIndex"(IN "TableName" VARCHAR(100),
                                IN "TypeName" VARCHAR(100),
                                OUT "TypeId" INTEGER)
  SPECIFIC "GetTypeIndex_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "TypeIndex" INTEGER DEFAULT NULL;
    SET "TypeIndex" = SELECT "Type" FROM "Types" WHERE "Name"="TypeName";
    IF "TypeIndex" IS NULL THEN
      SET "TypeIndex" = SELECT "Type" FROM "TableType" JOIN "Tables"
        ON "TableType"."Table"="Tables"."Table"
          WHERE "TableType"."Default"=TRUE AND "Tables"."Name"="TableName";
      IF "TypeIndex" IS NULL THEN 
        INSERT INTO "Types" ("Name","Value") VALUES ("TypeName","TypeName");
        SET "TypeIndex" = IDENTITY();
      END IF;
    END IF;
    SET "TypeId" = "TypeIndex";
  END"""

    elif name == 'createMergePeople':
        query = """\
CREATE PROCEDURE "MergePeople"(IN "Prefix" VARCHAR(50),
                               IN "ResourceName" VARCHAR(100),
                               IN "GroupId" INTEGER,
                               IN "Time" TIMESTAMP(6),
                               IN "Deleted" BOOLEAN)
  SPECIFIC "MergePeople_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "PeopleResource" VARCHAR(100);
    SET "PeopleResource" = REPLACE("ResourceName", "Prefix");
    IF "Deleted"=TRUE THEN
      DELETE FROM "Peoples" WHERE "Resource"="PeopleResource";
    ELSEIF NOT EXISTS(SELECT "People" FROM "Peoples" WHERE "Resource"="PeopleResource") THEN 
      INSERT INTO "Peoples" ("Resource","TimeStamp") VALUES ("PeopleResource","Time");
      INSERT INTO "Connections" ("Group","People","TimeStamp") VALUES ("GroupId",IDENTITY(),"Time");
    END IF;
  END"""

    elif name == 'createUnTypedDataMerge':
        q = """\
CREATE PROCEDURE "Merge%(Table)s"(IN "Prefix" VARCHAR(50),
                                  IN "ResourceName" VARCHAR(100),
                                  IN "LabelName" VARCHAR(100),
                                  IN "Value" VARCHAR(100),
                                  IN "Time" TIMESTAMP(6))
  SPECIFIC "Merge%(Table)s_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "PeopleIndex","LabelIndex" INTEGER DEFAULT NULL;
    SET "PeopleIndex" = "GetPeopleIndex"("Prefix","ResourceName");
    SET "LabelIndex" = "GetLabelIndex"("LabelName");
    MERGE INTO "%(Table)s" USING
      (VALUES("PeopleIndex","LabelIndex","Value","Time")) AS vals(w,x,y,z)
      ON "%(Table)s"."People"=vals.w AND "%(Table)s"."Label"=vals.x
        WHEN MATCHED THEN UPDATE SET "Value"=vals.y, "TimeStamp"=vals.z
        WHEN NOT MATCHED THEN INSERT ("People","Label","Value","TimeStamp")
          VALUES vals.w, vals.x, vals.y, vals.z;
  END"""
        query = q % format

    elif name == 'createTypedDataMerge':
        q = """\
CREATE PROCEDURE "Merge%(Table)s"(IN "Prefix" VARCHAR(50),
                                  IN "ResourceName" VARCHAR(100),
                                  IN "LabelName" VARCHAR(100),
                                  IN "Value" VARCHAR(100),
                                  IN "Time" TIMESTAMP(6),
                                  IN "Table" VARCHAR(50),
                                  IN "TypeName" VARCHAR(100))
  SPECIFIC "Merge%(Table)s_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "PeopleIndex","TypeIndex","LabelIndex" INTEGER DEFAULT NULL;
    SET "PeopleIndex" = "GetPeopleIndex"("Prefix","ResourceName");
    CALL "GetTypeIndex"("Table","TypeName","TypeIndex");
    SET "LabelIndex" = "GetLabelIndex"("LabelName");
    MERGE INTO "%(Table)s" USING
      (VALUES("PeopleIndex","TypeIndex","LabelIndex","Value","Time")) AS vals(v,w,x,y,z)
      ON "%(Table)s"."People"=vals.v AND "%(Table)s"."Type"=vals.w AND "%(Table)s"."Label"=vals.x
        WHEN MATCHED THEN UPDATE SET "Value"=vals.y, "TimeStamp"=vals.z
        WHEN NOT MATCHED THEN INSERT ("People","Type","Label","Value","TimeStamp")
          VALUES vals.v, vals.w, vals.x, vals.y, vals.z;
  END"""
        query = q % format

    elif name == 'createMergeGroup':
        query = """\
CREATE PROCEDURE "MergeGroup"(IN "Prefix" VARCHAR(50),
                              IN "PeopleId" INTEGER,
                              IN "ResourceName" VARCHAR(100),
                              IN "GroupName" VARCHAR(100),
                              IN "Time" TIMESTAMP(6),
                              IN "Deleted" BOOLEAN)
  SPECIFIC "MergeGroup_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "GroupResource" VARCHAR(100);
    SET "GroupResource" = REPLACE("ResourceName", "Prefix");
    IF "Deleted"=TRUE THEN
      DELETE FROM "Groups" WHERE "People"="PeopleId" AND "Resource"="GroupResource";
    ELSE
      MERGE INTO "Groups" USING (VALUES("PeopleId","GroupResource","GroupName","Time"))
        AS vals(w,x,y,z) ON "Groups"."Resource"=vals.x
          WHEN MATCHED THEN UPDATE
            SET "People"=vals.w, "Name"=vals.y, "TimeStamp"=vals.z, "GroupSync"=FALSE
          WHEN NOT MATCHED THEN INSERT ("People","Resource","Name","TimeStamp")
            VALUES vals.w, vals.x, vals.y, vals.z;
    END IF;
  END"""

    elif name == 'createMergeConnection':
        q = """\
CREATE PROCEDURE "MergeConnection"(IN "GroupPrefix" VARCHAR(50),
                                   IN "PeoplePrefix" VARCHAR(50),
                                   IN "ResourceName" VARCHAR(100),
                                   IN "Time" TIMESTAMP(6),
                                   IN "Separator" VARCHAR(1),
                                   IN "MembersList" VARCHAR(15000))
  SPECIFIC "MergeConnection_1"
  MODIFIES SQL DATA
  BEGIN ATOMIC
    DECLARE "Index" INTEGER DEFAULT 1;
    DECLARE "Pattern" VARCHAR(5) DEFAULT '[^$]+';
    DECLARE "GroupId", "PeopleId" INTEGER;
    DECLARE "GroupResource", "PeopleResource" VARCHAR(100);
    DECLARE "MembersArray" VARCHAR(100) ARRAY[%s];
    SET "GroupResource" = REPLACE("ResourceName", "GroupPrefix");
    SELECT "Group" INTO "GroupId" FROM "Groups" WHERE "Resource"="GroupResource";
    DELETE FROM "Connections" WHERE "Group"="GroupId";
    SET "Pattern" = REPLACE("Pattern", '$', "Separator");
    SET "MembersArray" = REGEXP_SUBSTRING_ARRAY("MembersList", "Pattern");
    WHILE "Index" <= CARDINALITY("MembersArray") DO
      SET "PeopleResource" = REPLACE("MembersArray"["Index"], "PeoplePrefix");
      SELECT "People" INTO "PeopleId" FROM "Peoples" WHERE "Resource"="PeopleResource";
      INSERT INTO "Connections" ("Group","People","TimeStamp")
        VALUES ("GroupId","PeopleId","Time");
      SET "Index" = "Index" + 1;
    END WHILE;
    UPDATE "Groups" SET "GroupSync"=TRUE WHERE "Group"="GroupId";
  END"""
        query = q % g_member

# Get Procedure Query
    elif name == 'insertUser':
        query = 'CALL "InsertUser"(?,?,?)'
    elif name == 'mergePeople':
        query = 'CALL "MergePeople"(?,?,?,?,?)'
    elif name == 'mergeGroup':
        query = 'CALL "MergeGroup"(?,?,?,?,?,?)'
    elif name == 'mergeConnection':
        query = 'CALL "MergeConnection"(?,?,?,?,?,?)'
    elif name == 'mergePeopleData':
        if format['Type'] is None:
            q = 'CALL "Merge%(Table)s"(?,?,?,?,?)'
        else:
            q = 'CALL "Merge%(Table)s"(?,?,?,?,?,?,?)'
        query = q % format

# Logging Changes Queries
    elif name == 'loggingChanges':
        if format:
            query = 'SET FILES LOG TRUE'
        else:
            query = 'SET FILES LOG FALSE'

# Saves Changes Queries
    elif name == 'saveChanges':
        if format:
            query = 'CHECKPOINT DEFRAG'
        else:
            query = 'CHECKPOINT'

# ShutDown Queries
    elif name == 'shutdown':
        if format:
            query = 'SHUTDOWN COMPACT;'
        else:
            query = 'SHUTDOWN;'

    elif name == 'shutdownCompact':
        query = 'SHUTDOWN COMPACT;'

# Queries don't exist!!!
    else:
        query = None
        msg = getMessage(ctx, __name__, 101, name)
        logMessage(ctx, SEVERE, msg, 'dbqueries', 'getSqlQuery()')
    return query
