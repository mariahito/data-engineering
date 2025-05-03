/* Question 1*/
CREATE SCHEMA stackoverflow;

/* Question 2*/
CREATE TABLE stackoverflow.survey (
    ResponseId VARCHAR(5) PRIMARY KEY,
    MainBranch VARCHAR(77),
    Employment VARCHAR(212),
    RemoteWork VARCHAR(36),
    CodingActivities VARCHAR(137),
    EdLevel VARCHAR(82),
    LearnCode VARCHAR(274),
    LearnCodeOnline VARCHAR(372),
    LearnCodeCoursesCert VARCHAR(65),
    YearsCode VARCHAR(18),
    YearsCodePro VARCHAR(18),
    DevType VARCHAR(659),
    OrgSize VARCHAR(50),
    PurchaseInfluence VARCHAR(32),
    BuyNewTool VARCHAR(277),
    Country VARCHAR(52),
    Currency VARCHAR(43),
    CompTotal VARCHAR(16),
    CompFreq VARCHAR(7),
    LanguageHaveWorkedWith VARCHAR(264),
    LanguageWantToWorkWith VARCHAR(264),
    DatabaseHaveWorkedWith VARCHAR(181),
    DatabaseWantToWorkWith VARCHAR(181),
    PlatformHaveWorkedWith VARCHAR(164),
    PlatformWantToWorkWith VARCHAR(164),
    WebframeHaveWorkedWith VARCHAR(210),
    WebframeWantToWorkWith VARCHAR(210),
    MiscTechHaveWorkedWith VARCHAR(219),
    MiscTechWantToWorkWith VARCHAR(219),
    ToolsTechHaveWorkedWith VARCHAR(100),
    ToolsTechWantToWorkWith VARCHAR(100),
    NEWCollabToolsHaveWorkedWith VARCHAR(267),
    NEWCollabToolsWantToWorkWith VARCHAR(267),
    OpSysProfessionalUse VARCHAR(87),
    OpSysPersonalUse VARCHAR(87),
    VersionControlSystem VARCHAR(41),
    VCInteraction VARCHAR(106),
    VCHostingPersonalUse VARCHAR(1),
    VCHostingProfessionalUse VARCHAR(1),
    OfficeStackAsyncHaveWorkedWith VARCHAR(260),
    OfficeStackAsyncWantToWorkWith VARCHAR(260),
    OfficeStackSyncHaveWorkedWith VARCHAR(138),
    OfficeStackSyncWantToWorkWith VARCHAR(138),
    Blockchain VARCHAR(16),
    NEWSOSites VARCHAR(151),
    SOVisitFreq VARCHAR(35),
    SOAccount VARCHAR(23),
    SOPartFreq VARCHAR(50),
    SOComm VARCHAR(15),
    Age VARCHAR(18),
    Gender VARCHAR(82),
    Trans VARCHAR(22),
    Sexuality VARCHAR(78),
    Ethnicity VARCHAR(345),
    Accessibility VARCHAR(200),
    MentalHealth VARCHAR(322),
    TBranch VARCHAR(3),
    ICorPM VARCHAR(23),
    WorkExp VARCHAR(2),
    Knowledge_1 VARCHAR(26),
    Knowledge_2 VARCHAR(26),
    Knowledge_3 VARCHAR(26),
    Knowledge_4 VARCHAR(26),
    Knowledge_5 VARCHAR(26),
    Knowledge_6 VARCHAR(26),
    Knowledge_7 VARCHAR(26),
    Frequency_1 VARCHAR(17),
    Frequency_2 VARCHAR(17),
    Frequency_3 VARCHAR(17),
    TimeSearching VARCHAR(26),
    TimeAnswering VARCHAR(26),
    Onboarding VARCHAR(14),
    ProfessionalTech VARCHAR(233),
    TrueFalse_1 VARCHAR(3),
    TrueFalse_2 VARCHAR(3),
    TrueFalse_3 VARCHAR(3),
    SurveyLength VARCHAR(21),
    SurveyEase VARCHAR(26),
    ConvertedCompYearly VARCHAR(8)
);

/* Question 3*/
-- Change the data type for comptotal column to handle all values from csv file
ALTER TABLE stackoverflow.survey
  ALTER COLUMN CompTotal TYPE NUMERIC USING CompTotal::NUMERIC;

--Add line to handle null (NA) values in data
COPY stackoverflow.survey
FROM 'C:/Users/Maria/Documents/Data engineering/hw6/stack-overflow-developer-survey-2022/survey_results_public.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL 'NA');

/* Question 5*/
-- Calculate the median of the valid CompTotal values
SELECT CEIL(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CompTotal)) AS median_comptotal
FROM stackoverflow.survey
WHERE CompTotal < 1000000000000;

-- Create a CTE to calculate the median of valid CompTotal values
WITH median_cte AS (
    SELECT CEIL(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CompTotal)) AS median_comptotal
    FROM stackoverflow.survey
    WHERE CompTotal < 1000000000000
)
-- Update the CompTotal values that are anomalous
UPDATE stackoverflow.survey
SET CompTotal = (SELECT median_comptotal FROM median_cte)
WHERE CompTotal >= 1000000000000;

-- Calculate the mean of the updated CompTotal values and round it up to the nearest whole number
SELECT CEIL(AVG(CompTotal)) AS mean_comptotal
FROM stackoverflow.survey;








