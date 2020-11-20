DROP TABLE IF EXISTS puma_names_2010;

-- Create a table for the 2010 PUMA names data
CREATE TABLE puma_names_2010
(
    State_FIPS CHAR(2),
    State_Name CHAR(100),
    CPUMA0010 CHAR(4),
    PUMA CHAR(5),
    GEOID CHAR(7),
    GISJOIN CHAR(9),
    PUMA_Name CHAR(500)
);
