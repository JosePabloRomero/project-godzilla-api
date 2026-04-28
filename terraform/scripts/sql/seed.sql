-- Carga de datos mock para API de vehiculos
INSERT INTO vehicles (make, model, year, nickname)
VALUES
  ('Nissan', 'Skyline GT-R R34', 2002, 'Godzilla'),
  ('Toyota', 'Supra RZ A80', 1998, 'Shogun'),
  ('Mazda', 'RX-7 FD3S', 2001, 'Akuma Rotary'),
  ('Honda', 'Civic Type R EK9', 2000, 'Samurai');

SELECT * FROM vehicles;
