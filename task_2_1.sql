SELECT 
    user_id, 
    SUM(reward) AS total_reward_2022
FROM 
    reports
WHERE 
    user_id IN (
        SELECT 
            user_id 
        FROM 
            reports 
        WHERE 
            DATE_PART('year', created_at) = 2021
        GROUP BY 
            user_id
    )
    AND DATE_PART('year', created_at) = 2022
GROUP BY 
    user_id;