package lam.kanjiapp;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import org.json.JSONObject;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by tlaminator on 4/13/17.
 */

public class EntryItemArrayAdapter extends ArrayAdapter<EntryItem> {
    private final static String TAG = "EntryItemArrayAdapter";
    private final Context context;
    ArrayList<EntryItem> itemArray;

    public EntryItemArrayAdapter(Context ctx, ArrayList<EntryItem> itemArray) {
        super(ctx, R.layout.entry_item);
        this.context = ctx;
        this.itemArray = itemArray;
        Log.d(TAG, "Read " + itemArray.size() + " EntryItem objects");
    }

    public View getView(int position, View convertView, ViewGroup parent) {
        LayoutInflater inflater = (LayoutInflater) context
                .getSystemService(Context.LAYOUT_INFLATER_SERVICE);

        View rowView = inflater.inflate(R.layout.entry_item, parent, false);
        // TODO: layout each EntryItem here
        ArrayList<Object> kanjiReadings = (ArrayList<Object>) itemArray.get(position).
                getKanjiReadings();
        TextView textView = (TextView) rowView.findViewById(R.id.readings);
        StringBuilder sb = new StringBuilder();
        String textToSet = "";
        for (int i = 0; i < kanjiReadings.size(); i++) {
            // each item is HashMap {"word": "...", "reading": "..."}
            try {
                HashMap<String, String> item = (HashMap<String, String>) kanjiReadings.get(i);
                String kanji = item.get("word");
                String reading = item.get("reading");
                if (kanji == null) {
                    sb.append(reading + "\t");
                } else if (reading == null) {
                    sb.append(kanji + "\t");
                } else {
                    sb.append(kanji + " (" + reading + ")\t\t\t");
                }
            } catch(Exception e) {
                e.printStackTrace();
            } finally {
                textToSet = sb.toString();
            }
        }
        textToSet = sb.toString();
        textView.setText(textToSet);
        return rowView;
    }

    public int getCount() { return itemArray.size(); }
    public EntryItem getItem(int position) { return itemArray.get(position); }
    public long getItemId(int position) { return position; }
}
