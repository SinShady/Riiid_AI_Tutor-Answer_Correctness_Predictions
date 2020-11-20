DROP TABLE IF EXISTS ct_puma_xwalk;

-- Create a table for the census tract to puma geographic crosswalk data
CREATE TABLE ct_puma_xwalk
(
    STATEFP CHARACTER(2),
    COUNTYFP CHARACTER(3),
    TRACTCE CHARACTER(6),
    PUMA5CE CHARACTER(5)
);
