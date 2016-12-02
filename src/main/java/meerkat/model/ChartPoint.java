package meerkat.model;

/**
 * Created by vchomakov on 12/2/2016.
 */
public class ChartPoint {

   public long timestamp;
   public int crowdSize;

   public ChartPoint(long timestamp, int crowdSize) {
      this.timestamp = timestamp;
      this.crowdSize = crowdSize;
   }
}
