package meerkat;

import org.springframework.data.repository.CrudRepository;

import java.util.List;

/**
 * Created by vchomakov on 12/1/2016.
 */
public interface SensorEventRepository extends CrudRepository<SensorEvent, Long> {

   public List<SensorEvent> findFirst1BySensorTypeAndDeviceIdOrderByTimestampDesc(
         String sensorType, String deviceId);

   public List<SensorEvent>
      findBySensorTypeAndDeviceIdAndTimestampGreaterThanOrderByTimestampAsc(
         String sensorType,
         String deviceId,
         long timestamp);
}
