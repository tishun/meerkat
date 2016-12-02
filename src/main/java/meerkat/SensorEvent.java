package meerkat;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

/**
 * Created by vchomakov on 12/1/2016.
 */
@Entity
public class SensorEvent {

   @Id
   @GeneratedValue(strategy = GenerationType.AUTO)
   private Long id;
   private String sensorType;
   private String sensorReading;
   private Long timestamp;
   private String deviceId;

   protected SensorEvent() {}

   public SensorEvent(
         String sensorType,
         String sensorReading,
         Long timestamp,
         String deviceId) {
      this.sensorType = sensorType;
      this.sensorReading = sensorReading;
      this.timestamp = timestamp;
      this.deviceId = deviceId;
   }

   public String toString() {
      return String.format(
            "SensorEvent[sensorType=%s, sensorReading=%s, " +
                  "timestamp=%d, deviceId = %s]",
            sensorType,
            sensorReading,
            timestamp,
            deviceId);
   }

   public String getSensorReading() {
      return this.sensorReading;
   }
}
