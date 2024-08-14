{{
  config(
    materialized='table'
  )
}}

select 
    b.LEVEL,
    a.TOPIC,
    b.YEAR,
    count(a."articleName") as Number_of_articles,
    MIN(LENGTH(b.SUMMARY)) AS "Min_Length_Summary",
    MAX(LENGTH(b.SUMMARY)) AS "Max_Length_Summary",
    MIN(LENGTH(b."learningOutcomes")) AS "Min_Learning_Outcomes",
    MAX(LENGTH(b."learningOutcomes")) AS "Max_Learning_Outcomes"
    from ASSIGNMENT3.CFA_DATA.GROBID as a inner join ASSIGNMENT3.CFA_DATA.CFA as b on
    a."articleName" = b.TOPIC 
    group by
    b.LEVEL,
    a.TOPIC,
    b.YEAR
    order by
    b.LEVEL,
    b.YEAR