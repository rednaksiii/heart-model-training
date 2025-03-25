using UnityEngine;
using Unity.Barracuda;
using UnityEngine.UI;
using System.Collections.Generic;

public class YOLOBarracuda : MonoBehaviour
{
    public NNModel yoloModelAsset;
    public RawImage rawImageDisplay;
    public TextAsset labelsFile;
    public RectTransform boundingBoxContainer;
    public GameObject boundingBoxPrefab;

    private Model runtimeModel;
    private IWorker worker;
    private WebCamTexture webcamTexture;
    private string[] labels;

    private List<GameObject> boxPool = new List<GameObject>();

    void Start()
    {
        runtimeModel = ModelLoader.Load(yoloModelAsset);
        worker = WorkerFactory.CreateWorker(WorkerFactory.Type.Auto, runtimeModel);

        webcamTexture = new WebCamTexture();
        webcamTexture.Play();
        rawImageDisplay.texture = webcamTexture;

        labels = labelsFile.text.Split('\n');
    }

    void Update()
    {
        if (webcamTexture.width < 100) return;

        Texture2D inputTex = new Texture2D(webcamTexture.width, webcamTexture.height);
        inputTex.SetPixels(webcamTexture.GetPixels());
        inputTex.Apply();

        Tensor input = new Tensor(inputTex, channels: 3);

        worker.Execute(input);
        Tensor output = worker.PeekOutput();

        ShowDetections(output);

        input.Dispose();
        output.Dispose();
        Destroy(inputTex);
    }

    void ShowDetections(Tensor output)
    {
        // Clear previous boxes
        foreach (var box in boxPool) Destroy(box);
        boxPool.Clear();

        for (int i = 0; i < output.shape.length; i += 7)
        {
            float confidence = output[i + 2];
            if (confidence < 0.5f) continue;

            float x = output[i + 3];
            float y = output[i + 4];
            float w = output[i + 5];
            float h = output[i + 6];

            GameObject box = Instantiate(boundingBoxPrefab, boundingBoxContainer);
            box.GetComponent<RectTransform>().anchoredPosition = new Vector2(x, y);
            box.GetComponent<RectTransform>().sizeDelta = new Vector2(w, h);

            boxPool.Add(box);
        }
    }

    private void OnDestroy()
    {
        worker?.Dispose();
    }
}
