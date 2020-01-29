#!
# -*- coding: utf_8 -*-

from .dbconfig import g_csv


def getSqlQuery(name, format=None):

# Create Static Table Queries
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
        c2 = '"Name" VARCHAR(100) NOT NULL'
        c3 = '"Type" VARCHAR(100) NOT NULL'
        c4 = '"Table" VARCHAR(100) NOT NULL'
        c5 = '"Column" INTEGER NOT NULL'
        k1 = 'CONSTRAINT "UniqueFieldsName" UNIQUE("Name")'
        c = (c1, c2, c3, c4, c5, k1)
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

# Create Dynamic View Queries
    elif name == 'createView':
        query = 'CREATE VIEW "%s"(%s) AS SELECT %s FROM %s' % format

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

# Create Role Query
    elif name == 'createRole':
        query = 'CREATE ROLE "FRONT_END"'
# Grant Role Query
    elif name == 'grantRole':
        query = 'GRANT SELECT ON TABLE "AddressBook" TO "FRONT_END"'

# Create User Query
    elif name == 'createUser':
        query = 'CREATE USER "%s" PASSWORD \'%s\'' % format
# Grant User Query
    elif name == 'grantUser':
        query = 'GRANT "FRONT_END" TO "%s"' % format

# Get last IDENTITY value that was inserted into a table by the current session
    elif name == 'getIdentity':
        query = 'CALL IDENTITY();'

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
        s1 = '"T"."Table" AS "TableId"'
        s2 = '"TL"."Label" AS "LabelId"'
        s3 = '"TT"."Type" AS "TypeId"'
        s4 = '"T"."Name" AS "Table"'
        s5 = '"L"."Name" AS "Label"'
        s6 = '"T3"."Name" AS "Type"'
        s7 = 'CONCAT(COALESCE("T3"."Name",\'\'),COALESCE("TL"."View","L"."Name")) AS "View"'
        s8 = '"T1"."Name" AS "PrimaryTable"'
        s9 = '"C1"."Name" AS "PrimaryColumn"'
        s10 = '"T2"."Name" AS "ForeignTable"'
        s11 = '"C2"."Name" AS "ForeignColumn"'
        s = (s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11)
        f1 = '"Tables" AS "T", "Tables" AS "T1", "Tables" AS "T2"'
        f2 = 'JOIN "TableLabel" AS "TL" ON "T"."Table"="TL"."Table"'
        f3 = 'JOIN "Labels" AS "L" ON "TL"."Label"="L"."Label"'
        f4 = 'LEFT JOIN "TableType" AS "TT" ON "T"."Table"="TT"."Table"'
        f5 = 'LEFT JOIN "Types" AS "T3" ON "TT"."Type"="T3"."Type"'
        f6 = 'JOIN "Columns" AS "C1" ON "T1"."Identity"="C1"."Column"'
        f7 = 'JOIN "Columns" AS "C2" ON "T2"."Identity"="C2"."Column"'
        w = '"T1"."Identity"=0 AND "T2"."Identity"=5 AND "T"."Name"=? '
        f = (f1, f2, f3, f4, f5, f6, f7)
        p = (','.join(s), ' '.join(f), w)
        query = 'SELECT %s FROM %s WHERE %s ORDER BY "TableId","LabelId","TypeId"' % p
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
        query = 'SELECT %s FROM %s  ORDER BY "F"."Field"' % p

    elif name == 'getTypesIndex':
        query = 'SELECT "Value","Type" FROM "Types" ORDER BY "Type"'
    elif name == 'getTypesDefault':
        c1 = '"T2"."Name"'
        c2 = '"T1"."Type"'
        f1 = '"TableType" AS "T1"'
        f2 = 'JOIN "Tables" AS "T2" ON "T1"."Default"=TRUE AND "T1"."Table"="T2"."Table"'
        c = (c1, c2)
        f = (f1, f2)
        p = (','.join(c), ' '.join(f))
        query = 'SELECT %s FROM %s ORDER BY "T2"."Table"' % p
    elif name == 'getLabelIndex':
        query = 'SELECT "Name","Label" FROM "Labels" ORDER BY "Label"'

    elif name == 'getPrimaryField':
        s = 'COALESCE("Tables"."Name","Columns"."Name","Labels"."Name","Fields"."Name") AS "Name"'
        f1 = '"Fields" AS "F"'
        f2 = 'LEFT JOIN "Tables" ON "F"."Table"=%s AND "F"."Column"="Tables"."Table"'
        f3 = 'LEFT JOIN "Columns" ON "F"."Table"=%s AND "F"."Column"="Columns"."Column"'
        f4 = 'LEFT JOIN "Labels" ON "F"."Table"=%s AND "F"."Column"="Labels"."Label"'
        f5 = 'LEFT JOIN "Fields" ON "F"."Table"=%s AND "F"."Field"="Fields"."Field"'
        f = (f1, f2 % "'Tables'", f3 % "'Columns'", f4 % "'Labels'", f5 % "'Loop'")
        w = '"F"."Type"=%s AND "F"."Table"=%s' % ("'Primary'","'Columns'")
        p = (s, ' '.join(f), w)
        query = 'SELECT %s FROM %s WHERE %s' % p
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
    elif name == 'getPeopleIndex':
        query = 'SELECT "Resource","People" FROM "Peoples" ORDER BY "People"'
    elif name == 'getPerson':
        query = 'SELECT "People","Resource","Account","Token" FROM "Peoples" WHERE "Account"=?'

# Insert Queries
    elif name == 'insertPerson':
        columns = '"Resource","Account"'
        values = '?,?'
        query = 'INSERT INTO "Peoples" (%s) VALUES (%s)' % (columns, values)
    elif name == 'insertPeople':
        columns = '"Resource"'
        values = '?'
        query = 'INSERT INTO "Peoples" (%s) VALUES (%s)' % (columns, values)
    elif name == 'insertConnection':
        columns = '"People","Connection"'
        values = '?,?'
        query = 'INSERT INTO "Connections" (%s) VALUES (%s)' % (columns, values)
    elif name == 'insertTypes':
        columns = '"Name","Value"'
        values = '?,?'
        query = 'INSERT INTO "Types" (%s) VALUES (%s)' % (columns, values)

# Update Queries
    elif name == 'updatePeoples':
        query = 'UPDATE "Peoples" SET "TimeStamp"=? WHERE "Resource"=?'
    elif name == 'updateToken':
        query = 'UPDATE "Peoples" SET "Token"=?,"TimeStamp"=? WHERE "People"=?'

# Get DataBase Version Query
    elif name == 'getVerion':
        query = 'Select DISTINCT DATABASE_VERSION() as "HSQL Version" From INFORMATION_SCHEMA.SYSTEM_TABLES'

# ShutDown Queries
    elif name == 'shutdown':
        query = 'SHUTDOWN;'
    elif name == 'shutdownCompact':
        query = 'SHUTDOWN COMPACT;'

# Queries don't exist!!!
    else:
        print("dbqueries.getSqlQuery(): ERROR: Query '%s' not found!!!" % name)
    return query
