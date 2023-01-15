package org.sample;
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.BenchmarkMode;
import org.openjdk.jmh.annotations.Fork;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.annotations.OutputTimeUnit;
import java.util.concurrent.TimeUnit;
import org.openjdk.jmh.annotations.Warmup;
import org.openjdk.jmh.annotations.Measurement;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;
public class MyBenchmark {

    private static final Logger logger = LogManager.getLogger(MyBenchmark.class);

    int binarySearch(int a[], int left, int right, int x) {
        if (right >= left) {
            int middle = left + (right-left)/2;
            if (a[middle] == x) return middle;
            else if (a[middle] > x) return binarySearch(a, left, middle - 1, x);
            else return binarySearch(a, middle+1, right, x);
        }
        return -1;
    }

    int[] getArray() {
        int[] arr = new int[1000000];
        for (int i = 0; i < 1000000; i++) {
            arr[i] = i;
        }
        return arr;
    }

    @Benchmark
    @BenchmarkMode(Mode.Throughput)
    @OutputTimeUnit(TimeUnit.MILLISECONDS)
    @Fork(value=1)
    @Warmup(iterations=0)
    @Measurement(iterations=5)
    public void testMethod() {
        logger.error("Method entry: " + System.nanoTime());
        int[] items = getArray();
        int found = binarySearch(items, 0, 9999, 7575);
        logger.error("Method exit: " + System.nanoTime());
    }
}
