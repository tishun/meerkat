package meerkat;

import com.sun.org.apache.xpath.internal.operations.Bool;
import meerkat.model.ChartPoint;
import org.springframework.format.annotation.NumberFormat;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class StatsController {

   private SensorEventRepository _repository;

   public StatsController(SensorEventRepository repository) {
      _repository = repository;
   }

   @RequestMapping("/stats")
   public Response stats(
         @RequestParam(value = "SENSOR_TYPE", required = false) String sensorType,
         @RequestParam(value = "SENSOR_READING", required = false) String sensorReading,
         @RequestParam(value = "TIMESTAMP", required = false, defaultValue = "0") String
               timestamp,
         @RequestParam(value = "DEVICE_ID", required = false) String deviceId,
         @RequestParam(value = "TOKEN", required = true) String token) {

      if (!token.equals("2416ca72-827c-4e33-afef-aa68271ba982")) {
         return new Response("Unauthorized!");
      }

      SensorEvent sensorEvent =
            new SensorEvent(sensorType, sensorReading, Long.valueOf(timestamp),
                  deviceId);

      String createdObject = sensorEvent.toString();
      System.out.println(createdObject);

      _repository.save(sensorEvent);

      System.out.println("Current number of customers: " + _repository.count());

      return new Response("Received: " + createdObject);
   }

   @RequestMapping("/availability")
   public Response availability() {

      List<SensorEvent> fitnessSoundEvent =
            _repository.findFirst1BySensorTypeAndDeviceIdOrderByTimestampDesc(
                  "SND", "fitness");
      String fitnessStatus = "unknown";
      if (!fitnessSoundEvent.isEmpty() && fitnessSoundEvent.size() == 1) {
         SensorEvent event = fitnessSoundEvent.get(0);
         fitnessStatus = event.getSensorReading();
      }
      return new Response("Current fitness state: " + fitnessStatus);
   }

   @RequestMapping("/availability/{room}")
   public Boolean availabilityPerRoom(@PathVariable String room) {

      List<SensorEvent> lastEvent =
            _repository.findFirst1BySensorTypeAndDeviceIdOrderByTimestampDesc(
                  "CAM", room);
      // It is safer to declare a room available than not.
      boolean status = true;
      if (!lastEvent.isEmpty() && lastEvent.size() == 1) {
         SensorEvent event = lastEvent.get(0);
         if (event.getSensorReading().equals("1")) {
            // 1 Volt means unavailable
            status = false;
         }
      }
      return status;
   }

   @RequestMapping("/crowd/{room}")
   public int crowdPerRoom(@PathVariable String room) {

      List<SensorEvent> lastCamEvent =
            _repository.findFirst1BySensorTypeAndDeviceIdOrderByTimestampDesc(
                  "CAM", room);
      int numberOfBlobs = 0;
      if (!lastCamEvent.isEmpty() && lastCamEvent.size() == 1) {
         SensorEvent event = lastCamEvent.get(0);
         if (event != null && event.getSensorReading() != null) {
            try {
               numberOfBlobs = Integer.parseInt(event.getSensorReading());
            } catch (NumberFormatException e) {
               System.out.println("Error parsing CAM input: " +
                     event.getSensorReading());
            }
         }
      }
      return numberOfBlobs;
   }

//   @RequestMapping("/historical/{room}/daily")
//   public ChartPoint[] historicalRoomDaily(@PathVariable String room) {
//      List<SensorEvent> lastCamEvent =
//            _repository.findFirst1BySensorTypeAndDeviceIdOrderByTimestampDesc(
//                  "CAM", room);
//   }
}
