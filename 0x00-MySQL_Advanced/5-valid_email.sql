--Trigger to ret attribute valid_email when email has been changed
delimiter |

CREATE TRIGGER valid_email BEFORE UPDATE ON users
       FOR EACH ROW
       BEGIN
           IF NEW.email != OLD.email THEN
               SET NEW.valid_email = 0;
           END IF;
       END
|
