package lam.kanjiapp;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 * Created by tlaminator on 4/4/17.
 */

public class EntryFragment extends Fragment {
    private static final String TAG = "EntryFragment";
    public static final String SELECTED_ENTRY_ITEM_READINGS = "ENTRY_ITEM_READINGS";
    public static final String SELECTED_ENTRY_ITEM_DEFINITIONS = "ENTRY_ITEM_DEFINITIONS";
    View v;
    ImageView imageV;
    ListView entryLV;
    ArrayList<EntryItem> entryItemArrayList;

    public EntryFragment() {
        // Required empty public constructor
    }

    public static EntryFragment newInstance(String param1, String param2) {
        EntryFragment fragment = new EntryFragment();
        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        v = inflater.inflate(R.layout.fragment_entry, container, false);
        imageV = (ImageView) v.findViewById(R.id.image_id);
        entryLV = (ListView) v.findViewById(R.id.entry_list_view);

        entryLV.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                EntryItem item = (EntryItem) parent.getItemAtPosition(position);
                ArrayList<Object> kanjiReadings = (ArrayList<Object>) item.getKanjiReadings();
                ArrayList<Object> definitions = (ArrayList<Object>) item.getDefinitions();


                Intent intent = new Intent(getActivity(), EntryDetailActivity.class);
                intent.putExtra(SELECTED_ENTRY_ITEM_READINGS, kanjiReadings);
                intent.putExtra(SELECTED_ENTRY_ITEM_DEFINITIONS, definitions);
                startActivity(intent);
            }
        });
        return v;
    }

    public void setImage(Bitmap image) {
        imageV.setImageBitmap(image);
    }

    public void setEntryItemArrayList(JSONObject obj) {
        try {
            Log.d(TAG, obj.get("data").getClass().toString());
            JSONArray data = (JSONArray) obj.get("data");
            Log.d(TAG, data.toString(4));

            entryItemArrayList = new ArrayList<>();

            for (int i = 0; i < data.length(); i++) {
                EntryItem newItem = new EntryItem();

                JSONObject entryJSON = (JSONObject) data.get(i);

                JSONArray readingsArray = (JSONArray) entryJSON.get("japanese");
                newItem.setKanjiReadings(toList(readingsArray));

                JSONArray sensesArray = (JSONArray) entryJSON.get("senses");
                newItem.setDefinitions(toList(sensesArray));

                if (i == 0) {
                    HashMap<String, String> item = (HashMap<String, String>)
                            newItem.getKanjiReadings().get(0);
                    String resultKanjiStr = item.get("word");
                    TextView resultKanjiTV = (TextView) v.findViewById(R.id.result_kanji);
                    resultKanjiTV.setText(resultKanjiStr);
                    resultKanjiTV.setTextSize(100);
                }
                entryItemArrayList.add(newItem);
            }
            EntryItemArrayAdapter adapter = new EntryItemArrayAdapter(getActivity(),
                    entryItemArrayList);
            entryLV.setAdapter(adapter);
            adapter.notifyDataSetChanged();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static Map<String, Object> toMap(JSONObject object) throws JSONException {
        Map<String, Object> map = new HashMap<String, Object>();

        Iterator<String> keysItr = object.keys();
        while(keysItr.hasNext()) {
            String key = keysItr.next();
            Object value = object.get(key);

            if(value instanceof JSONArray) {
                value = toList((JSONArray) value);
            }

            else if(value instanceof JSONObject) {
                value = toMap((JSONObject) value);
            }
            map.put(key, value);
        }
        return map;
    }

    public static List<Object> toList(JSONArray array) throws JSONException {
        List<Object> list = new ArrayList<Object>();
        for(int i = 0; i < array.length(); i++) {
            Object value = array.get(i);
            if(value instanceof JSONArray) {
                value = toList((JSONArray) value);
            }

            else if(value instanceof JSONObject) {
                value = toMap((JSONObject) value);
            }
            list.add(value);
        }
        return list;
    }
}
