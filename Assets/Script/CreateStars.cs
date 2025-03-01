using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using UnityEngine;
using Debug = UnityEngine.Debug;

public class CreateStars : MonoBehaviour
{
    public GameObject starPrefab;
    public GameObject parent;
    public string path;
    // Start is called before the first frame update
    public void test()
    {
        Debug.Log("test");
    }
    public void GenerateStars()
    {
        StreamReader reader = null;
        string strCmdText;
        strCmdText= "/K cd C:\\Users\\caban\\NasaSpaceAppChallenge\\Python & .venv\\Scripts\\activate & python gaiaquery.py 18_Del_b";

        System.Diagnostics.Process.Start("CMD.exe",strCmdText);
        if (File.Exists(path))
        {
            reader = new StreamReader(File.OpenRead(path));
            while (!reader.EndOfStream)
            {
                var line = reader.ReadLine();
                var values = line.Split(',');
                float X = float.Parse(values[0]);
                float Y = float.Parse(values[1]);
                float Z = float.Parse(values[2]);
                float Brighness = float.Parse(values[3]);
                GameObject.Instantiate(starPrefab, new Vector3(X, Y, Z), Quaternion.identity, parent.transform);
            }
            reader.Close();
        }
        else
        {
            Debug.Log("File is not generated");
        }
    }
}
