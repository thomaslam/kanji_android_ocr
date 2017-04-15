package lam.kanjiapp;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.provider.MediaStore;
import android.provider.Settings;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";
    public static final int MY_PERMISSIONS_REQUEST_CAMERA = 100;
    public static final int PHOTO_TAKEN_REQUEST = 1;
    public static final String ALLOW_KEY = "ALLOWED";
    public static final String CAMERA_PREF = "camera_pref";
    private final static int COMPRESSION_QUALITY = 100;
    public final static String OWN_SERVER_URL = "http://148.85.253.96:15675";
    public final static String ENTRY_URL = "http://jisho.org/api/v1/search/words?keyword=";

    Button mCamera;
    FragmentManager manager;
    EntryFragment entryFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final Activity context = this;

        manager = getSupportFragmentManager();
        FragmentTransaction transaction = manager.beginTransaction();

        if (entryFragment == null) {
            entryFragment = new EntryFragment();
            transaction.add(R.id.entry_fragment_container, entryFragment).commit();
        }

        mCamera = (Button) findViewById(R.id.camera_btn);

        mCamera.setOnClickListener( new View.OnClickListener()
        {
            public void onClick (View v) {
                if (ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA)
                        != PackageManager.PERMISSION_GRANTED) {
                    if (getFromPref(context, ALLOW_KEY)) {
                        showSettingsAlert(context);
                    } else if (ContextCompat.checkSelfPermission(context,
                            Manifest.permission.CAMERA)

                            != PackageManager.PERMISSION_GRANTED) {

                        // Should we show an explanation?
                        if (ActivityCompat.shouldShowRequestPermissionRationale(context,
                                Manifest.permission.CAMERA)) {
                            showAlert();
                        } else {
                            // No explanation needed, we can request the permission.
                            ActivityCompat.requestPermissions(context,
                                    new String[]{Manifest.permission.CAMERA},
                                    MY_PERMISSIONS_REQUEST_CAMERA);
                        }
                    }
                } else {
                    openCamera();
                }
            }
        });
    }

    public static Boolean getFromPref(Context context, String key) {
        SharedPreferences myPrefs = context.getSharedPreferences(CAMERA_PREF,
                Context.MODE_PRIVATE);
        return (myPrefs.getBoolean(key, false));
    }

    private void showSettingsAlert(final Activity context) {
        AlertDialog alertDialog = new AlertDialog.Builder(context).create();
        alertDialog.setTitle("Alert");
        alertDialog.setMessage("App needs to access the Camera.");

        alertDialog.setButton(AlertDialog.BUTTON_NEGATIVE, "DONT ALLOW",
                new DialogInterface.OnClickListener() {

                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                        //finish();
                    }
                });

        alertDialog.setButton(AlertDialog.BUTTON_POSITIVE, "SETTINGS",
                new DialogInterface.OnClickListener() {

                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                        startInstalledAppDetailsActivity(context);
                    }
                });

        alertDialog.show();
    }

    public static void startInstalledAppDetailsActivity(final Activity context) {
        if (context == null) {
            return;
        }

        final Intent i = new Intent();
        i.setAction(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
        i.addCategory(Intent.CATEGORY_DEFAULT);
        i.setData(Uri.parse("package:" + context.getPackageName()));
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        i.addFlags(Intent.FLAG_ACTIVITY_NO_HISTORY);
        i.addFlags(Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS);
        context.startActivity(i);
    }

    private void showAlert() {
        AlertDialog alertDialog = new AlertDialog.Builder(this).create();
        alertDialog.setTitle("Alert");
        alertDialog.setMessage("App needs to access the Camera.");
        final Activity context = this;

        alertDialog.setButton(AlertDialog.BUTTON_NEGATIVE, "DONT ALLOW",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                        context.finish();
                    }
                });

        alertDialog.setButton(AlertDialog.BUTTON_POSITIVE, "ALLOW",
                new DialogInterface.OnClickListener() {

                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                        ActivityCompat.requestPermissions(context,
                                new String[]{Manifest.permission.CAMERA},
                                MY_PERMISSIONS_REQUEST_CAMERA);
                    }
                });
        alertDialog.show();
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode == Activity.RESULT_OK) {
            if (requestCode == PHOTO_TAKEN_REQUEST) {
                if (data != null) {
                    try {
                        Bundle extras = data.getExtras();
                        Bitmap imageBitmap = (Bitmap) extras.get("data");

                        // TODO: sends image to server for classifying using AsyncTask
                        JSONObject toSend = new JSONObject();
                        toSend.put("photo", getStringFromBitmap(imageBitmap));
                        new SendPicTask().execute(toSend);
                        // diplays image in ImageView in EntryFragment
                        entryFragment.setImage(imageBitmap);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }

                } else {
                    Log.d(TAG, "intent data is null");
                }
            }
        }
    }

    private String getStringFromBitmap(Bitmap bitmapPicture) {
        String encodedImage;
        ByteArrayOutputStream byteArrayBitmapStream = new ByteArrayOutputStream();
        bitmapPicture.compress(Bitmap.CompressFormat.PNG, COMPRESSION_QUALITY,
                byteArrayBitmapStream);
        byte[] b = byteArrayBitmapStream.toByteArray();
        encodedImage = Base64.encodeToString(b, Base64.DEFAULT);
        return encodedImage;
    }

    private void openCamera() {
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (intent.resolveActivity(this.getPackageManager()) != null) {
            startActivityForResult(intent, PHOTO_TAKEN_REQUEST);
        }
    }

    private class GetEntryTask extends AsyncTask<URL, Void, JSONObject> {
        protected JSONObject doInBackground(URL... urls) {
            HttpURLConnection urlConnection = null;
            JSONObject resultEntry = null;
            try {
                Log.d(TAG, "in doInBackground of GetEntryTask");
                URL url = urls[0];

                urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("GET");

                urlConnection.connect();

                int status = urlConnection.getResponseCode();
                Log.d(TAG, "Response code: " + status);

                if (status == 200 || status == 201) {
                    Log.d(TAG, "Got entry");
                    BufferedReader br = new BufferedReader(
                            new InputStreamReader(urlConnection.getInputStream()));
                    StringBuilder sb = new StringBuilder();
                    String line;
                    while ((line = br.readLine()) != null) {
                        sb.append(line);
                    }
                    br.close();

                    resultEntry = new JSONObject(sb.toString());
                    Log.d(TAG, sb.toString());
                } else {
                    Log.d(TAG, "Can't get entry");
                }
                resultEntry.put("status", status);
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                urlConnection.disconnect();
            }
            return resultEntry;
        }

        protected void onPostExecute(JSONObject result) {
            try {
                if (result.getInt("status") == 200 || result.getInt("status") == 201) {
                    entryFragment.setEntryItemArrayList(result);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    private class SendPicTask extends AsyncTask<JSONObject, Void, JSONObject> {
        protected JSONObject doInBackground(JSONObject... objs) {
            HttpURLConnection urlConnection = null;
            JSONObject result = new JSONObject();
            String parsedCode = "";
            try {
                Log.d(TAG, "in doInBackground of SendPicTask");
                JSONObject jsonObject = objs[0];

                URL url = new URL(OWN_SERVER_URL);

                // Create an http connection to communicate with url
                urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestProperty("Content-Type", "application/json");
                urlConnection.setRequestProperty("Accept", "application/json");
                urlConnection.setRequestMethod("POST");

                OutputStream os = urlConnection.getOutputStream();
                os.write(jsonObject.toString().getBytes("UTF-8"));
                os.close();

                // Connect to url
                urlConnection.connect();
                int status = urlConnection.getResponseCode();
                Log.d(TAG, "Response code: " + status);

                if (status == 200 || status == 201) {
                    Log.d(TAG, "Successfully sent pic to server");

                    BufferedReader br = new BufferedReader(
                            new InputStreamReader(urlConnection.getInputStream()));
                    StringBuilder sb = new StringBuilder();
                    String line;
                    while ((line = br.readLine()) != null) {
                        sb.append(line);
                    }
                    br.close();

                    JSONObject resultJSON = new JSONObject(sb.toString());
                    parsedCode = resultJSON.getString("parsedCode");
                    Log.d(TAG, "parsedCode is " + parsedCode);
                } else {
                    Toast toast = Toast.makeText(getApplicationContext(),
                            "Fail to send pic to server", Toast.LENGTH_SHORT);
                    toast.show();
                }

                // Prepare json for GetEntryTask
                result.put("status", status);
                result.put("parsedCode", parsedCode);
            } catch(Exception e) {
                e.printStackTrace();
            } finally {
                urlConnection.disconnect();
            }
            return result;
        }

        protected void onPostExecute(JSONObject result) {
            try {
                if (result.getInt("status") == 200 || result.getInt("status") == 201) {
                    URL entryURL = new URL(ENTRY_URL + result.get("parsedCode"));
                    new GetEntryTask().execute(entryURL);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
