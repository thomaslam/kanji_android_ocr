package lam.kanjiapp;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * Created by tlaminator on 4/12/17.
 */

public class EntryItem {
    private List<Object> kanjiReadings;
    private List<Object> definitions;


    public List<Object> getKanjiReadings() {
        return this.kanjiReadings;
    }

    public List<Object> getDefinitions() {
        return this.definitions;
    }

    public void setDefinitions(List<Object> definitions) {
        this.definitions = definitions;
    }

    public void setKanjiReadings(List<Object> map) {
        this.kanjiReadings = map;
    }
}
