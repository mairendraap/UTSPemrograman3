CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    score NUMERIC(5,2) NOT NULL,
    risk VARCHAR(20) NOT NULL
);

INSERT INTO students (name, score, risk) VALUES
('Andi', 72, 'LOW_RISK'),
('Budi', 48, 'HIGH_RISK'),
('Citra', 86, 'LOW_RISK'),
('Dewi', 55, 'HIGH_RISK'),
('Eko', 67, 'LOW_RISK'),
('Fajar', 41, 'HIGH_RISK');
