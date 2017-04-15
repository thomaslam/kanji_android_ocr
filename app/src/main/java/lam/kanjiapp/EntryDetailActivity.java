package lam.kanjiapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.ListView;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * Created by tlaminator on 4/14/17.
 */

public class EntryDetailActivity extends AppCompatActivity {
    private static final String TAG = "EntryDetailActivity";
    private ArrayList<Object> readings;
    private ArrayList<Object> definitions;
    private Intent intent;

    ArrayList<DefinitionItem> dItems;
    ListView definitionLV;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_entry_detail);
        definitionLV = (ListView) findViewById(R.id.definition_list_view);

        intent = getIntent();
        readings = (ArrayList<Object>) intent.getSerializableExtra(
                EntryFragment.SELECTED_ENTRY_ITEM_READINGS);
        definitions = (ArrayList<Object>) intent.getSerializableExtra(
                EntryFragment.SELECTED_ENTRY_ITEM_DEFINITIONS);

        Log.d(TAG, "readings: " + readings.toString());
        Log.d(TAG, "definitions: " + definitions.toString());

        setDefinitionLV(definitions);
    }

    public void setDefinitionLV(ArrayList<Object> definitions) {
        try {
            dItems = new ArrayList<>();

            for (int i = 0; i < definitions.size(); i++) {
                DefinitionItem newDefItem = new DefinitionItem();

                // TODO: initialize newDefItem
                HashMap sense = (HashMap) definitions.get(i);
                ArrayList<String> engDefs = (ArrayList<String>) sense.get("english_definitions");
                ArrayList<String> posStrs = (ArrayList<String>) sense.get("parts_of_speech");

                String def = getStringFromArrayListStr(engDefs);
                String pos = getStringFromArrayListStr(posStrs);

                newDefItem.setDefinition(def);
                newDefItem.setPOS(pos);
                dItems.add(newDefItem);
            }

            DefinitionItemArrayAdapter adapter = new DefinitionItemArrayAdapter(this, dItems);
            definitionLV.setAdapter(adapter);
            adapter.notifyDataSetChanged();
        } catch(Exception e) {
            e.printStackTrace();
        }
    }

    public String getStringFromArrayListStr(ArrayList<String> arr) {
        StringBuilder sb = new StringBuilder();
        if (arr.size() == 0) {
            return "";
        }
        for (int j = 0; j < arr.size()-1; j++) {
            String s = arr.get(j);
            sb.append(s + "; ");
        }
        sb.append(arr.get(arr.size()-1));
        return sb.toString();
    }
}
