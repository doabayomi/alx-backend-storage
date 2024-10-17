-- Trigger that decreases item qty after a new order
DROP TRIGGER IF EXISTS reduce_quantity;
DELIMITER $$
CREATE TRIGGER reduce_qty
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
END $$
DELIMITER ;
