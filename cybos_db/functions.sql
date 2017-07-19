
DROP FUNCTION IF EXISTS cybos.numeric_only;

DELIMITER $$
CREATE FUNCTION cybos.numeric_only (val VARCHAR(255))
 RETURNS VARCHAR(255)
BEGIN
 DECLARE idx INT DEFAULT 0;
 IF ISNULL(val) THEN RETURN NULL; END IF;

 IF LENGTH(val) = 0 THEN RETURN ""; END IF;

 SET idx = LENGTH(val);
  WHILE idx > 0 DO
  IF IsNumeric(SUBSTRING(val,idx,1)) = 0 THEN
   SET val = REPLACE(val,SUBSTRING(val,idx,1),"");
   SET idx = LENGTH(val)+1;
  END IF;
  SET idx = idx - 1;
  END WHILE;
  RETURN CAST(val as UNSIGNED);
 END;
 $$
DELIMITER ;
 DROP FUNCTION IF EXISTS IsNumeric;
DELIMITER $$
CREATE FUNCTION IsNumeric (val varchar(255)) RETURNS tinyint
 RETURN val REGEXP '^(-|\\+){0,1}([0-9]+\\.[0-9]*|[0-9]*\\.[0-9]+|[0-9]+)$';
 $$
 DELIMITER ;