import java.util.List;
public class SentimentAnalysis {
	public static void main(String[] args) {
		StanfordCoreNLP stanfordCoreNLP = Pipeline.getPipeline();

		String text = "hello this is john. i don't like this place";

		CoreDocument coreDocument = new CoreDocument(text);

		stanfordCoreNLP.annotate(coreDocument);

		List<CoreSentence> sentences = coreDocument.sentences();

		for(CoreSentence s : sentences) {
			String sentiment = s.sentiment();
			System.out.println(sentiment + '\t' + s)
		}
	}


// Different File
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import java.util.Properties;

public class Pipeline {
	private static Properties properties;
	private static String propertiesName = "tokenize, parse, sentiment, ner";
	private static StanfordCoreNLP stanfordCoreNLP;

	private Pipeline() {

	}

	static {
		properties = new Properties();
		properties.setProperty("annotators", propertiesName);
	}

	public static StanfordCoreNLP getPipeline() {
		if(stanfordCoreNLP == null) {
			stanfordCoreNLP = new StanfordCoreNLP(properties);
		}
		return stanfordCoreNLP;
	}
}