-- ─────────────────────────────────────────────────────────
--  Aptitude AI  ·  Database Schema + Seed Data
-- ─────────────────────────────────────────────────────────

CREATE DATABASE IF NOT EXISTS 'Afridi2008$aptitude_ai';
USE 'Afridi2008$aptitude_ai';

-- Users
CREATE TABLE IF NOT EXISTS users (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    email    VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(64)  NOT NULL,
    created  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions
CREATE TABLE IF NOT EXISTS questions (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    topic    VARCHAR(50) NOT NULL,
    question TEXT        NOT NULL,
    option1  TEXT        NOT NULL,
    option2  TEXT        NOT NULL,
    option3  TEXT        NOT NULL,
    option4  TEXT        NOT NULL,
    answer   VARCHAR(10) NOT NULL   -- stores "option1" | "option2" | "option3" | "option4"
);

-- Quiz Results (per attempt)
CREATE TABLE IF NOT EXISTS results (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    score           INT NOT NULL,
    total_questions INT NOT NULL,
    date            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Per-question breakdown
CREATE TABLE IF NOT EXISTS result_answers (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    result_id  INT         NOT NULL,
    topic      VARCHAR(50) NOT NULL,
    is_correct TINYINT(1)  NOT NULL DEFAULT 0,
    FOREIGN KEY (result_id) REFERENCES results(id)
);

-- ─── Seed: Sample Questions ────────────────────────────────

INSERT INTO questions (topic, question, option1, option2, option3, option4, answer) VALUES

-- Percentages
('Percentages', 'What is 20% of 200?', '20', '40', '60', '80', 'option2'),
('Percentages', 'A shirt costs ₹500. A 15% discount is applied. What is the selling price?', '₹400', '₹425', '₹450', '₹475', 'option2'),
('Percentages', 'If a value increases from 80 to 100, what is the percentage increase?', '20%', '25%', '15%', '10%', 'option2'),

-- Ratios
('Ratios', 'The ratio of boys to girls in a class is 3:2. If there are 30 boys, how many girls are there?', '15', '18', '20', '25', 'option3'),
('Ratios', 'Divide ₹720 in the ratio 3:5. What is the larger share?', '₹270', '₹360', '₹450', '₹480', 'option3'),

-- Speed & Distance
('Speed & Distance', 'A car travels 150 km in 3 hours. What is its average speed?', '45 km/h', '50 km/h', '55 km/h', '60 km/h', 'option2'),
('Speed & Distance', 'Two trains of length 100m and 150m approach each other at 60 km/h and 40 km/h. How long to cross?', '9 sec', '10 sec', '11 sec', '12 sec', 'option2'),

-- Time & Work
('Time & Work', 'A can finish a job in 10 days, B in 15 days. Working together, how many days?', '4', '5', '6', '8', 'option3'),
('Time & Work', 'If 8 workers complete a project in 12 days, how many workers are needed to finish it in 6 days?', '12', '14', '16', '18', 'option3'),

-- Probability
('Probability', 'A bag has 3 red and 5 blue balls. What is the probability of picking a red ball?', '1/4', '3/8', '5/8', '1/2', 'option2'),
('Probability', 'A fair die is rolled. What is the probability of getting an even number?', '1/6', '1/3', '1/2', '2/3', 'option3'),

-- Logical Reasoning
('Logical Reasoning', 'If all cats are animals and all animals are living things, are all cats living things?', 'Yes', 'No', 'Cannot determine', 'Sometimes', 'option1'),
('Logical Reasoning', 'In a sequence: 2, 6, 12, 20, 30, __ — what comes next?', '40', '42', '44', '46', 'option2'),

-- Verbal
('Verbal', 'Choose the synonym of BENEVOLENT:', 'Kind', 'Cruel', 'Indifferent', 'Greedy', 'option1'),
('Verbal', 'Choose the antonym of ABUNDANT:', 'Plentiful', 'Scarce', 'Rich', 'Ample', 'option2');
