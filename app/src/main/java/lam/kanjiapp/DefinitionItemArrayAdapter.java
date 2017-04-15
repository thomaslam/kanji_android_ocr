package lam.kanjiapp;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Created by tlaminator on 4/14/17.
 */

public class DefinitionItemArrayAdapter extends ArrayAdapter<DefinitionItem> {
    private final static String TAG = "DIArrayAdapter";
    private final Context context;
    ArrayList<DefinitionItem> itemArray;

    public DefinitionItemArrayAdapter(Context ctx, ArrayList<DefinitionItem> itemArray) {
        super(ctx, R.layout.definition_item);
        this.context = ctx;
        this.itemArray = itemArray;
        Log.d(TAG, "Read " + itemArray.size() + " EntryItem objects");
    }

    public View getView(int position, View convertView, ViewGroup parent) {
        LayoutInflater inflater = (LayoutInflater) context
                .getSystemService(Context.LAYOUT_INFLATER_SERVICE);

        View rowView = inflater.inflate(R.layout.definition_item, parent, false);
        TextView defTV = (TextView) rowView.findViewById(R.id.definition_text);
        TextView posTV = (TextView) rowView.findViewById(R.id.pos_text);

        DefinitionItem item = itemArray.get(position);

        defTV.setText("Def: " + item.getDefinition());
        posTV.setText("POS: " + item.getPOS());
        return rowView;
    }

    public int getCount() { return itemArray.size(); }
    public DefinitionItem getItem(int position) { return itemArray.get(position); }
    public long getItemId(int position) { return position; }
}
